"""
Image Generation Module
Generates images from text prompts using Hugging Face models
Optimized for CPU inference with caching and fast generation
"""

import os
import hashlib
from io import BytesIO
from PIL import Image


class ImageGenerator:
    """Generate images from text prompts using Hugging Face models"""
    
    def __init__(self, model_id="runwayml/stable-diffusion-v1-5", cache_dir=None):
        """
        Initialize the image generator
        
        Args:
            model_id: Hugging Face model ID for image generation
                     Default: runwayml/stable-diffusion-v1-5 (fast, open-access)
            cache_dir: Directory to cache generated images
        """
        self.model_id = model_id
        self.pipe = None
        self.cache_dir = cache_dir or os.path.join(os.path.dirname(__file__), "..", "..", ".cache", "images")
        os.makedirs(self.cache_dir, exist_ok=True)
        self._initialize_model()
    
    def _initialize_model(self):
        """Initialize the Hugging Face pipeline with CPU optimizations"""
        try:
            from diffusers import StableDiffusionPipeline
            import torch
            
            # Check if GPU is available
            device = "cuda" if torch.cuda.is_available() else "cpu"
            
            print(f"Loading {self.model_id} on {device}...")
            print("Optimizing for fast inference...")
            
            # Use float32 on CPU (float16 doesn't work on CPU)
            if device == "cuda":
                torch_dtype = torch.float16
            else:
                torch_dtype = torch.float32
            
            self.pipe = StableDiffusionPipeline.from_pretrained(
                self.model_id,
                dtype=torch_dtype,  # Use dtype instead of torch_dtype
                safety_checker=None  # Disable safety checker to speed up
            )
            self.pipe = self.pipe.to(device)
            
            # Enable memory optimizations for faster inference
            self.pipe.enable_attention_slicing()
            
            print(f"Model loaded and optimized on {device}")
        
        except Exception as e:
            print(f"Error loading model: {e}")
            print("Falling back to placeholder image generation")
            self.pipe = None
    
    def _get_cache_path(self, prompt, num_steps, guidance):
        """Generate cache file path based on prompt hash"""
        cache_key = f"{prompt}_{num_steps}_{guidance}"
        hash_name = hashlib.md5(cache_key.encode()).hexdigest()
        return os.path.join(self.cache_dir, f"{hash_name}.png")
    
    def generate_image(self, prompt, num_inference_steps=20, guidance_scale=7.0):
        """
        Generate an image from a text prompt
        
        Args:
            prompt: Text description of the image to generate
            num_inference_steps: Number of inference steps (20-30 recommended)
            guidance_scale: Guidance scale for controlling prompt adherence
        
        Returns:
            PIL Image object or None if generation fails
        """
        if not prompt or not isinstance(prompt, str):
            return None
        
        # Check cache first
        cache_path = self._get_cache_path(prompt, num_inference_steps, guidance_scale)
        if os.path.exists(cache_path):
            print(f"Loading image from cache")
            try:
                return Image.open(cache_path)
            except Exception as cache_err:
                print(f"Cache load failed: {cache_err}, regenerating...")
        
        try:
            if self.pipe is None:
                print("Pipeline not available, using placeholder")
                return self._generate_placeholder(prompt)
            
            # Generate image with optimizations
            print(f"Generating image: '{prompt[:50]}...' ({num_inference_steps} steps)")
            
            image = self.pipe(
                prompt=prompt,
                num_inference_steps=num_inference_steps,
                guidance_scale=guidance_scale,
                height=512,
                width=512
            ).images[0]
            
            # Cache the generated image
            try:
                os.makedirs(os.path.dirname(cache_path), exist_ok=True)
                image.save(cache_path)
                print(f"Cached image successfully")
            except Exception as cache_save_err:
                print(f"Cache save failed (non-critical): {cache_save_err}")
            
            return image
        
        except Exception as e:
            print(f"Error generating image: {e}")
            print("Using placeholder image instead")
            return self._generate_placeholder(prompt)
    
    def _generate_placeholder(self, prompt):
        """Generate a placeholder image when real generation fails"""
        try:
            # Create a simple placeholder image with text
            from PIL import ImageDraw, ImageFont
            
            width, height = 512, 512
            image = Image.new('RGB', (width, height), color=(100, 100, 100))
            draw = ImageDraw.Draw(image)
            
            # Add text to placeholder
            text = f"Image for:\n\n{prompt[:60]}..." if len(prompt) > 60 else f"Image for:\n\n{prompt}"
            
            # Simple text drawing (without font to avoid file not found errors)
            draw.text((50, 200), text, fill=(255, 255, 255))
            
            return image
        
        except Exception as e:
            print(f"Error creating placeholder: {e}")
            return None
    
    def generate_batch(self, prompts, num_inference_steps=50, guidance_scale=7.5):
        """
        Generate multiple images from prompts
        
        Args:
            prompts: List of text prompts
            num_inference_steps: Number of inference steps
            guidance_scale: Guidance scale for prompt adherence
        
        Returns:
            List of PIL Image objects
        """
        images = []
        for prompt in prompts:
            img = self.generate_image(prompt, num_inference_steps, guidance_scale)
            if img:
                images.append((prompt, img))
        
        return images


def generate_query_visualization_prompts(query_response):
    """
    Generate visualization prompts based on query response
    
    Args:
        query_response: The response from the knowledge graph query
    
    Returns:
        List of image generation prompts
    """
    prompts = []
    
    # Extract key terms from response for image generation
    keywords = [
        "financial planning", "investment", "savings", "loan",
        "budget", "vehicle purchase", "decision making", "growth"
    ]
    
    for keyword in keywords:
        if keyword.lower() in query_response.lower():
            # Create a descriptive prompt for visualization
            prompt = f"Professional infographic about {keyword} with charts, graphs, and icons, clean design, minimalist"
            prompts.append(prompt)
    
    # If no specific keywords found, generate a generic financial visualization
    if not prompts:
        prompts.append("Modern financial analysis dashboard with data visualization, professional design")
    
    return prompts[:3]  # Limit to 3 prompts

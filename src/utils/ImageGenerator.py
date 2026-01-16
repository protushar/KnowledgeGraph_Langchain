"""
Image Generation Module
Generates images from text prompts using Hugging Face models
"""

import os
from io import BytesIO
from PIL import Image


class ImageGenerator:
    """Generate images from text prompts using Hugging Face models"""
    
    def __init__(self, model_id="runwayml/stable-diffusion-v1-5"):
        """
        Initialize the image generator
        
        Args:
            model_id: Hugging Face model ID for image generation
                     Default: runwayml/stable-diffusion-v1-5 (open-access, no auth required)
        """
        self.model_id = model_id
        self.pipe = None
        self._initialize_model()
    
    def _initialize_model(self):
        """Initialize the Hugging Face pipeline"""
        try:
            from diffusers import StableDiffusionPipeline
            import torch
            
            # Check if GPU is available
            device = "cuda" if torch.cuda.is_available() else "cpu"
            
            print(f"Loading {self.model_id} on {device}...")
            print("First load may take a few minutes as the model downloads (~4GB)...")
            
            self.pipe = StableDiffusionPipeline.from_pretrained(
                self.model_id,
                torch_dtype=torch.float32,
                use_auth_token=False  # Explicitly don't require auth for open models
            )
            self.pipe = self.pipe.to(device)
            
            # Enable memory optimizations
            if device == "cpu":
                self.pipe.enable_attention_slicing()
            else:
                self.pipe.enable_attention_slicing()
            
            print(f"Model loaded successfully on {device}")
        
        except Exception as e:
            print(f"Error loading model: {e}")
            print("Falling back to placeholder image generation")
            self.pipe = None
    
    def generate_image(self, prompt, num_inference_steps=50, guidance_scale=7.5):
        """
        Generate an image from a text prompt
        
        Args:
            prompt: Text description of the image to generate
            num_inference_steps: Number of inference steps (higher = better quality, slower)
            guidance_scale: Guidance scale for controlling prompt adherence
        
        Returns:
            PIL Image object or None if generation fails
        """
        if not prompt or not isinstance(prompt, str):
            return None
        
        try:
            if self.pipe is None:
                return self._generate_placeholder(prompt)
            
            # Generate image
            print(f"Generating image from prompt: {prompt}")
            
            image = self.pipe(
                prompt=prompt,
                num_inference_steps=num_inference_steps,
                guidance_scale=guidance_scale
            ).images[0]
            
            return image
        
        except Exception as e:
            print(f"Error generating image: {e}")
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

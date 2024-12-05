from typing import Dict, Any, Optional

def format_context(context: Optional[Dict[str, Any]]) -> str:
    """
    Format the context data into a string for the AI model.
    
    Args:
        context: Dictionary containing page and product information
        
    Returns:
        Formatted string containing relevant context information
    """
    if not context:
        return ""
    
    formatted = []
    
    if 'pageData' in context and context['pageData']:
        product = context['pageData'].get('productInfo', {})
        if product:
            formatted.extend([
                f"Product: {product.get('title', 'N/A')}",
                f"Price: {product.get('price', 'N/A')}",
                f"Rating: {product.get('rating', 'N/A')}",
                f"Description: {product.get('description', 'N/A')}"
            ])
    
    if 'url' in context:
        formatted.append(f"Current URL: {context['url']}")
        
    if 'cookies' in context and context['cookies']:
        cart_items = [
            cookie for cookie in context['cookies'] 
            if 'cart' in cookie.get('name', '').lower()
        ]
        if cart_items:
            formatted.append("Shopping Cart: Items detected")
    
    return "\n".join(formatted) if formatted else "No context available"

import re
from typing import Dict, List

class EmailMarketingUtils:
    @staticmethod
    def validate_email(email: str) -> bool:
        """
        Validate email format
        """
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        return bool(re.match(pattern, email))

    @staticmethod
    def calculate_metrics(campaign_data: Dict) -> Dict:
        """
        Calculate key email marketing metrics
        """
        total_sent = campaign_data.get('sent', 0)
        opens = campaign_data.get('opens', 0)
        clicks = campaign_data.get('clicks', 0)
        conversions = campaign_data.get('conversions', 0)

        metrics = {
            'open_rate': (opens / total_sent * 100) if total_sent > 0 else 0,
            'click_rate': (clicks / opens * 100) if opens > 0 else 0,
            'conversion_rate': (conversions / clicks * 100) if clicks > 0 else 0,
            'total_sent': total_sent
        }
        
        return metrics

    @staticmethod
    def segment_audience(subscribers: List[Dict], criteria: Dict) -> List[Dict]:
        """
        Segment email list based on given criteria
        """
        segmented_list = []
        
        for subscriber in subscribers:
            matches = all(
                subscriber.get(key) == value 
                for key, value in criteria.items()
            )
            if matches:
                segmented_list.append(subscriber)
                
        return segmented_list

    @staticmethod
    def generate_html_template(content: Dict) -> str:
        """
        Generate basic HTML email template
        """
        template = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>{content.get('subject', '')}</title>
        </head>
        <body>
            <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                <h1>{content.get('headline', '')}</h1>
                <div>{content.get('body', '')}</div>
                <div style="margin-top: 20px;">
                    <a href="{content.get('cta_link', '#')}" 
                       style="background-color: #007bff; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">
                        {content.get('cta_text', 'Click Here')}
                    </a>
                </div>
            </div>
        </body>
        </html>
        """
        return template 
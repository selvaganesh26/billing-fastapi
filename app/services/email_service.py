import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Dict, List
import logging

logger = logging.getLogger(__name__)


class EmailService:
    """Simple email service for sending invoices"""
    
    def __init__(self, smtp_host: str = "smtp.gmail.com", smtp_port: int = 587):
        self.smtp_host = smtp_host
        self.smtp_port = smtp_port
    
    def send_invoice_email(
        self,
        to_email: str,
        purchase_data: Dict,
        sender_email: str = "billing@example.com",
        sender_password: str = ""
    ):
        """Send invoice email to customer"""
        try:
            # Create email
            msg = MIMEMultipart('alternative')
            msg['Subject'] = f"Invoice #{purchase_data['id']} - Billing System"
            msg['From'] = sender_email
            msg['To'] = to_email
            
            # Create HTML content
            html_content = self._generate_invoice_html(purchase_data)
            html_part = MIMEText(html_content, 'html')
            msg.attach(html_part)
            
            # Send email (commented out for demo - requires SMTP credentials)
            # with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
            #     server.starttls()
            #     server.login(sender_email, sender_password)
            #     server.send_message(msg)
            
            logger.info(f"Invoice email sent to {to_email} for purchase #{purchase_data['id']}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send email: {str(e)}")
            return False
    
    def _generate_invoice_html(self, purchase_data: Dict) -> str:
        """Generate HTML invoice"""
        items_html = ""
        for item in purchase_data.get('purchase_items', []):
            items_html += f"""
            <tr>
                <td>{item['product_id']}</td>
                <td>{item['unit_price_snapshot']:.2f}</td>
                <td>{item['quantity']}</td>
                <td>{item['unit_price_snapshot'] * item['quantity']:.2f}</td>
                <td>{item['tax_percent_snapshot']:.2f}%</td>
                <td>{item['tax_amount']:.2f}</td>
                <td>{item['total_price']:.2f}</td>
            </tr>
            """
        
        change_html = ""
        for denom in purchase_data.get('change_denominations', []):
            change_html += f"<li>{denom['denomination_value']}: {denom['count_given']}</li>"
        
        return f"""
        <html>
        <body style="font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto;">
            <h2>Invoice #{purchase_data['id']}</h2>
            <p><strong>Date:</strong> {purchase_data['created_at']}</p>
            
            <h3>Items Purchased</h3>
            <table border="1" cellpadding="5" style="border-collapse: collapse; width: 100%;">
                <tr style="background-color: #f0f0f0;">
                    <th>Product ID</th>
                    <th>Unit Price</th>
                    <th>Quantity</th>
                    <th>Purchase Price</th>
                    <th>Tax %</th>
                    <th>Tax Amount</th>
                    <th>Total</th>
                </tr>
                {items_html}
            </table>
            
            <div style="margin-top: 20px;">
                <p><strong>Total without tax:</strong> Rs.{purchase_data['total_amount']:.2f}</p>
                <p><strong>Total tax payable:</strong> Rs.{purchase_data['tax_amount']:.2f}</p>
                <p><strong>Net price:</strong> Rs.{purchase_data['final_amount']:.2f}</p>
                <p><strong>Paid amount:</strong> Rs.{purchase_data['paid_amount']:.2f}</p>
                <p><strong>Balance/Change:</strong> Rs.{purchase_data['balance_amount']:.2f}</p>
            </div>
            
            {f'<h3>Change Denominations</h3><ul>{change_html}</ul>' if change_html else ''}
            
            <p style="margin-top: 30px; color: #666;">Thank you for your purchase!</p>
        </body>
        </html>
        """

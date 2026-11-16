import json
import boto3
import uuid
from datetime import datetime

dynamodb = boto3.resource('dynamodb')
sns = boto3.client('sns')

TABLE_NAME = 'HelpdeskSystem2026'
SNS_TOPIC_ARN = '[กรอก-SNS-TOPIC-ARN-ของคุณตรงนี้]'

def lambda_handler(event, context):
    try:
        raw_body = event.get('body', '{}')
        body = json.loads(raw_body) if isinstance(raw_body, str) else raw_body
        
        name = body.get('name', 'ไม่ระบุชื่อ')
        room = body.get('room', 'ไม่ระบุห้อง')
        issue = body.get('issue', 'ไม่มีรายละเอียด')
        
        ticket_id = f"TCK-{str(uuid.uuid4())[:8]}"
        created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        table = dynamodb.Table(TABLE_NAME)
        item = {
            'TicketID': ticket_id,
            'Name': name,
            'Room': room,
            'Issue': issue,
            'Status': 'Pending',
            'CreatedAt': created_at
        }
        
        table.put_item(Item=item)
        
        message_body = (
            f"🔔 มีรายการแจ้งซ่อมใหม่!\n\n"
            f"Ticket ID: {ticket_id}\n"
            f"ผู้แจ้ง: {name}\n"
            f"ห้อง/สถานที่: {room}\n"
            f"รายละเอียด: {issue}\n"
            f"เวลาที่แจ้ง: {created_at}\n"
        )
        
        sns.publish(
            TopicArn=SNS_TOPIC_ARN,
            Subject=f"[Helpdesk Alert] Ticket ใหม่ {ticket_id}",
            Message=message_body
        )
        
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Methods': 'OPTIONS,POST'
            },
            'body': json.dumps({'message': 'สร้าง Ticket สำเร็จ!', 'ticket_id': ticket_id})
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({'error': str(e)})
        }

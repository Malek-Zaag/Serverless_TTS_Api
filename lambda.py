import json
import boto3
import base64

def generateAudioFromText(text):
    polly= boto3.client('polly')
    response= polly.synthesize_speech(  Text=text,
                                        TextType = "text",
                                        OutputFormat='mp3', 
                                        VoiceId='Bianca')
    audio_stream = response['AudioStream'].read()
    audio_base64 = base64.b64encode(audio_stream).decode('utf-8')
    bucket_name = "serverless-api-bucket24"
    filename = "audios/audio.mp3"
    bucket = boto3.client('s3').put_object(Bucket=bucket_name, Key=filename, Body=audio_stream)
    return audio_base64
    
def lambda_handler(event, context):
    # TODO implement
    audio_base64 = generateAudioFromText("Hello world!, My name is Malek and I am a cloud Engineer, nice to meet you!")
    return {
        'statusCode': 200,
        #'body': json.dumps(base64.b64encode(response).decode('utf-8')+)
        'headers': {
                'Content-Type': 'audio/mpeg',
            },
        'body': audio_base64,
        'isBase64Encoded': True
    }

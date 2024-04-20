import json
import boto3
import base64
import time

textToConvert=""

def generateAudioFromText(text):
    polly= boto3.client('polly')
    response= polly.synthesize_speech(  Text=text,
                                        TextType = "text",
                                        LanguageCode= "en-US",
                                        OutputFormat='mp3', 
                                        VoiceId='Bianca')
    audio_stream = response['AudioStream'].read()
    audio_base64 = base64.b64encode(audio_stream).decode('utf-8')
    bucket_name = "serverless-api-bucket24"
    filename = "audios/audio.mp3"
    bucket = boto3.client('s3').put_object(Bucket=bucket_name, Key=filename, Body=audio_stream)
    return audio_base64
    
    
def getTextToConvert(text):
    global textToConvert
    textToConvert= text
    
def lambda_handler(event, context):
    #audio_base64 = generateAudioFromText("Hello world!, My name is Malek and I am a cloud Engineer, nice to meet you!")
    try:
        print(event)
        print(textToConvert)
        request=event.get("requestContext").get("http").get("method")
        #request= event['httpMethod']
        if request == "GET":
            return {
                'statusCode': 200,
                'headers': {
                        'Content-Type': 'audio/mpeg',
                    },
                # 'body': audio_base64 | None,
                'body': generateAudioFromText(textToConvert),
                'isBase64Encoded': True 
            }
        elif request == "POST":
            getTextToConvert(event.get("body"))
            #audio_base64= generateAudioFromText(text)
            return {
                'statusCode': 200,
                'headers': {
                    'Content-Type': 'application/json',
                },
                'body': "Text to convert was uploaded successfully"
            }
        else :
            return {
                'statusCode': 404,
                'headers': {
                    'Content-Type': 'application/json',
                },
                'body': event
            }
    except Exception as e:
        return {
            'statusCode': 200,
            'headers': {
                    'Content-Type': 'application/json',
                },
            'body': json.dumps(str(e))
        }
        
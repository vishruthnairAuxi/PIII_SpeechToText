

import subprocess
import speech_recognition as sr
import shlex
import os
from ibm_watson import SpeechToTextV1


r = sr.Recognizer()
m = sr.Microphone()


f = open("sp_to_text.txt", "w")

f1 = open("sp_text_ds.txt", "w")
try:
    with m as source: r.adjust_for_ambient_noise(source)
    print("Set minimum energy threshold to {}".format(r.energy_threshold))
    while True:
        print("Say something!")
        with m as source: audio = r.listen(source)
        print("Got it")
        try:
            #recognize speech using Google Speech Recognition
            value = r.recognize_google(audio)   

            if str is bytes:  
                print(u"You said {}".format(value).encode("utf-8"))
            else:  #
                print("You said {}".format(value))

            if value=="stop":
                break
            f.write(value)
            f.write("\n")


            ##deepspeech
            # with open("microphone-results.wav", "wb") as f1:
            #     f1.write(audio.get_wav_data())


            # cmd = 'python client.py --model deepspeech-0.7.4-models.pbmm --scorer deepspeech-0.7.4-models.scorer --audio microphone-results.wav'
    
            # os.system(cmd)
            # output = subprocess.call(shlex.split(cmd)) 

        except sr.UnknownValueError:
            print("Oops! Didn't catch that")
        except sr.RequestError as e:
            print("Uh oh! Couldn't request results from Google Speech Recognition service; {0}".format(e))


        # # recognize speech using Google Cloud Speech           
        try:
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="gckey.json"   
            recog = r.recognize_google_cloud(audio)
            print("google cloudYou said: " + recog)
        except sr.UnknownValueError as u:
            print(u)
            print("Google Cloud Speech Recognition could not understand audio")
        except sr.RequestError as e:
            print("Could not request results from Google Cloud Speech Recognition service; {0}".format(e))  



        
        import threading
        from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

        authenticator = IAMAuthenticator('l47xyObdt6es3LXDtLwxQ7Dx48MlbOW9q_aE8GGEaPFS')
        service = SpeechToTextV1(authenticator=authenticator)
        service.set_service_url('https://api.us-east.speech-to-text.watson.cloud.ibm.com/instances/a8ca96a5-90fd-446f-bce5-8bf03f85c3a')

        models = service.list_models().get_result()
        print(json.dumps(models, indent=2))

        model = service.get_model('en-US_BroadbandModel').get_result()
        print(json.dumps(model, indent=2))

        
        print(json.dumps(
            service.recognize(
                audio=audio,
                content_type='audio/wav',
                timestamps=True,
                word_confidence=True).get_result(),
            indent=2))


except KeyboardInterrupt:
    pass

print("stopped listening")

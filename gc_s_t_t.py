

import subprocess
import speech_recognition as sr
import shlex
import os
from ibm_watson import SpeechToTextV1


r = sr.Recognizer()
m = sr.Microphone()


# import pyttsx3
# engine = pyttsx3.init()
# engine.say("I will speak this text")
# engine.runAndWait()



try:
    with m as source: r.adjust_for_ambient_noise(source)
    
    print("Set minimum energy threshold to {}".format(r.energy_threshold)) 
    print("Say something!")
    with m as source: audio = r.listen(source)
    print("Got it")
        

    # # recognize speech using Google Cloud Speech           
    try:
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="gckey.json"   
        recog = r.recognize_google_cloud(audio, preferred_phrases=["pie chart", "team slide", "bar chart", "stop"])
        print("you said: " + recog)


        if "team slide" in recog:
            print("team slide being built now")
            words = recog.split(" ")

            for i in range (len(words)):
                if "slide" == words[i]:
                    break

            people = words[i+2:]
            data = {
                    "req": "create_team_slide",
                    "people": people
                }


        elif "pie chart" in recog:
            
            while True:

                print("enter details (Say Stop to finish)")
                try:
                    with m as source: audio = r.listen(source)
                    recog = r.recognize_google_cloud(audio)
                    recog = recog.strip()
                    if "stop" in recog:
                        break
                    
                    if "change" in recog:
                        words = recog.split(" ")

                    else:
                        words = recog.split(" ")
                        print(words)
                        categories=[]
                        percentages = []
                        for i in range(0,len(words),2): 
                            categories.append(words[i])
                            percentages.append(words[i+1])
                
                except sr.UnknownValueError as u:
                        print("Google Cloud Speech Recognition could not understand speech, please repeat statement")


            data = {
                        "req": "create_pie_chart",
                        "categories": categories,
                        "percentages": percentages
                    }


        print(data)

    except sr.UnknownValueError as u:
        print("Google Cloud Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Cloud Speech Recognition service; {0}".format(e))  


    
except KeyboardInterrupt:
    pass

print("stopped listening")

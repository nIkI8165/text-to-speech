import gtts
import pyttsx3
from sys import stdin

# directly or indirectly
way = input("Do you want to open a file or input text directly? Enter 'file' or 'input': ")
match way:
    case 'file':
        # attempt to open file from user-input
        path = input("Enter a valid pathname to a file: ")
        try:
            file = open(path, encoding='utf-8', mode="r")
        except FileNotFoundError:
            print(path, "is not a valid pathname to a file.")
            quit()
        # merging lines
        lines = file.readlines()
        for i in range(len(lines)):
            lines[i] = lines[i].rstrip()
        lines = ' '.join(lines)
        file.close()
    case 'input':
        print("Input your text here. When ready, type 'exit' or 'quit' on a new line.")
        lines = []
        for line in stdin:
            if 'exit' == line.rstrip() or 'quit' == line.rstrip():
                break
            lines.append(line.rstrip())
        lines = ' '.join(lines)
        print(lines)
    case _:
        print(way, "is not an option.")
        quit()
# name of the file in which the result will be saved
name = input("Enter a name for the file in which you want the result to be saved, followed by .mp3: ")
if '.' in name:
    if name[name.find('.'):] != '.mp3':
        print(name[name.find('.'):], "is an invalid file extension.")
        quit()
else:
    print("The file must have an extension.")
    quit()
# online or offline
onoff = input("Online or offline processing? Enter 'online' or 'offline': ")
match onoff:
    case 'online':
        # set a language
        language = input("What language is the text in? Enter 'ru', 'en' or 'de': ")
        # set a tempo
        tempo = input("Do you want the speech to be faster or slower? Enter 'faster' or 'slower': ")
        match tempo:
            case 'faster':
                t_bool = False
            case 'slower':
                t_bool = True
            case _:
                print(tempo, "is not an option.")
                quit()
        # make request to google to get synthesis
        match language:
            case 'ru':
                tts = gtts.gTTS(lines, lang="ru", slow=t_bool)
            case 'en':
                tts = gtts.gTTS(lines, lang="en", slow=t_bool)
            case 'de':
                tts = gtts.gTTS(lines, lang="de", slow=t_bool)
            case _:
                print(language, "is not an option.")
                quit()
        # saving to a file
        tts.save(name)
    case 'offline':
        # initializing TTS engine
        engine = pyttsx3.init()
        # get all voices
        voices = engine.getProperty("voices")
        # set a language
        language = input("What language is the text in? Enter 'ru', 'en' or 'de': ")
        match language:
            case 'ru':
                engine.setProperty("voice", voices[0].id)
            case 'en':
                # set a voice (only available in English)
                sex = input("Do you want it to be a male or female voice? Enter 'male' or 'female': ")
                match sex:
                    case 'male':
                        engine.setProperty("voice", voices[1].id)
                    case 'female':
                        engine.setProperty("voice", voices[2].id)
                    case _:
                        print(sex, "is not an option.")
                        quit()
            case 'de':
                engine.setProperty("voice", voices[3].id)
            case _:
                print(language, "is not an option.")
                quit()
        # set a tempo
        tempo = int(input("At what tempo do you want your text to be read? Enter: "))
        engine.setProperty("rate", tempo)
        # saving to a file
        engine.save_to_file(lines, name)
        engine.runAndWait()
    case _:
        print(onoff, "is not an option.")
        quit()
# work completion notification
print(f"Processed! The result's saved as {name}.")

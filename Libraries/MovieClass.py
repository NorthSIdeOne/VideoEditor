from moviepy.editor import *
from moviepy.video.tools.subtitles import SubtitlesClip
import re # module for regular expressions

class Movie:
    def __init__(self,url):
        self.url = url
        self.clip = VideoFileClip(url)
        self.result = None

    def cut(self,t1,t2,name):
        try:
            time = self.clip.duration

            """
                Variabila "time" este utilizata pentru salvarea duratei videoclipului.

                Practic, prin intermediul acestei variabile verific ca datele ce sunt utilizate prntru decupare,
                adica timpul de start si timpul de stop, sunt valide si nu depasesc durata videoclipului.

                Daca datele sunt valide atunci incepe procesul de decupare al videoclipului. Functia de biblioteca 
                subclip(t1,t2) realizeaza aceasta functionalitate, t1 fiind timpul de start, iar t2 timpul de stop.

                Astfel, secventa dorita din membrul self.clip (membru in care este salvat videoclipul) este salvata
                in membrul rezultat al clasei.

                Daca datele introduse nu sunt valide se afiseaza un mesaj corespunzator.
            """

            if(t1<time and t2<time and t1>=0 and t2>=0):
                self.result = self.clip.subclip(t1,t2)
                self.result.write_videofile(name)

            else:
                print("Parametrii pentru decupare nu sunt corecti.")
                print("Asigurativa ca cei doi parametrii sunt in concordanta cu durata videoclipului")

        except:
            print("Something went wrong with cut method")

    def concat(self,name,*video):
        try:
            self.result = concatenate_videoclips([self.clip, *video])
            self.result.write_videofile(name)

            """
                Metoda "concat" realizeaza concatenarea a doua sau mai multor videoclipuri.

                Obiectele de tip fisier video sunt primite ca parametru sub forma unei liste.

                Foarte important!!!
                Pentru ca procesul de concatenare sa fie realizat cu succes, toate videoclipurile
                ce se doresc a fi concatenate trebuie sa aiba aceeasi rezolutie.

                Daca conditia de mai sus nu este respectata procesul de concatenare va esua.
            """
        
        except:
            print("Something went wrong with concat method")

    def video_resize(self,quality,name):
        try:
            self.result = self.clip.resize(height = quality) 
            self.result.write_videofile(name)

            """
                Metoda video_resize modifica rezolutia obiectului de tip video.
                Rezolutia dorita este primita ca parametru in variabila "quality", iar numele
                fisierului rezultat este primit in variabila "name".

                Foarte important!!!
                Noua rezolutie, primita ca parametru, nu trebuie sa fie mai mare decat rezolutia
                videoclipului original. 
            """

        except:
            print("Something went wrong with video_resize method")

    def video_speed(self,fact,name):
        self.result = self.clip.speedx(fact) 
        #elf.result.speedx(self.clip,fact)
        self.result.write_videofile(name)

    def video_mirroring(self,name):
        try:
            self.result = self.clip.fx(vfx.mirror_x)
            self.result.write_videofile(name)

            """
                Metoda "video_mirroring" creaza un nou videoclip, care este in oglinda fata de
                videoclipul original. Pentru acest lucru este utilizata metoda fx(vfx.mirror_x)
            """

        except:
            print("Something went wrong with video_mirroring method")  
    
    def sound_replace(self,audio_file,out_name,mode):
        try:
            # async = modul de apelare utilizat atunci cand fisierul audio are o durata diferita fata de cel audio
            if mode =="async":
                audio = AudioFileClip(audio_file)	
                time = self.clip.duration
                self.result = concatenate_videoclips([self.clip]).set_audio(audio)
                self.result = self.result.subclip(0,time)
                self.result.write_videofile(out_name)
        
            # sync = modul de apelare utilizat atunci cand fisierul audio si cel audio au aceeasi durata
            elif mode =="sync":
                audio = AudioFileClip(audio_file)	
                time = self.clip.duration
                self.result = concatenate_videoclips([self.clip]).set_audio(audio)
                #self.result = self.result.subclip(0,time)
                self.result.write_videofile(out_name)

            # custom_async = modul de apelare utilizat atunci cand utilizatorul doreste adaugarea noii coloane sonore peste cea existenta, nu inlocuirea completa a acesteia,
            #                iar durata celor doua fisiere nu este egala
            elif mode == "custom_sync":
                audio = AudioFileClip(audio_file)

                new_audioclip = CompositeAudioClip([self.clip.audio, audio])
                self.clip.audio = new_audioclip
            
                self.clip.write_videofile(out_name)

            # custom_sync = modul de apelare utilizat atunci cand utilizatorul doreste adaugarea noii coloane sonore peste cea existenta, nu inlocuirea completa a acesteia,
            #                iar durata celor doua fisiere este egala
            elif mode == "custom_async":
           
                audio_f = AudioFileClip(audio_file)
                time = self.clip.duration
            
                new_audioclip = CompositeAudioClip([self.clip.audio, audio_f])
                self.clip.audio = new_audioclip
           
                self.result = self.clip.subclip(0,time)
                self.result.write_videofile(out_name)

                """
                    Metoda "sound_replace" modifica coloana sonora a videoclipului.
                    Aceasta metoda suporta mai multe moduri, cum ar fi: "async","sync","custom_async","custom_sync".
                    Functionalitatea acestora a fost explicata mai sus.

                    Metoda suporta si adaugarea unei coloane sonore peste cea existenta, dar si inlocuirea completa
                    a acesteia.

                """

        except:
            print("Something went wrong with sound_replace method")  
            
    def get_frame(self,time,name):
        try:
            video_duration = self.clip.duration
            if video_duration < time:
                print("Valoarea introdusa este prea mare. Durata videoclipului selectat este ",video_duration)
            else:
                self.clip.save_frame(name, t=time)

            """
                Metoda "get_frame" permite capturarea unui cadru din videoclipul selectat. Acest lucru se face
                pe baza parametrului "time" in care se specifica momentul de timp la caare se regaseste cadrul
                ce se doreste a fi capturat.

                Foarte important!!!
                Pentru o functionare buna a acestei metode, parametrul "time" nu trebuie sa depaseasca durata 
                videoclipului. In caz contrar se va afisa un mesaj corespunzator.
            """

        except:
            print("Something went wrong with get_frame method")   

    def add_subtitle(self,subtitle_file,out_name):
        try:
            generator = lambda txt: TextClip(txt, font='Times', fontsize=16, color='white')
            subtitles = SubtitlesClip(subtitle_file, generator)

            self.result = CompositeVideoClip([self.clip, subtitles.set_pos(('center','bottom'))])

            self.result.write_videofile(out_name, fps=self.clip.fps)

            """
                Metoda "add_subtitle" permite adaugarea de subtitrari in cadrul videoclipurilor. 

                Aceasta metoda se foloseste atat de biblioteca "Moviepy", aceasta punand la dispozitie
                metodele de scriere/citire a fisierelor video si clasa "SubtitlesClip" ce permite adaugarea
                subtitrarilor, dar se foloseste si de utilitarul "ImageMagickDisplay", acest utilitar 
                realizand procesul de adaugare a textului peste fisierul video.

                Dupa cum se poate observa mai sus, putem sa selectam fontul textului, dimensiunea acestuia,
                dar si culoarea acestuia.
            """

        except:
            print("Something went wrong with add_subtitle method")


    def find_sequence(self, words,subtitle_file,output):
        try:
            with open(subtitle_file) as f:
                lines = f.readlines()
            #deschid fisierul de subtitrare si salvez continutul in variabila lines
        except:
            print("Something went wrong with find_sequence method(open file)")

        try:
            times_texts = [] # lista in care voi salva textul si timpul corespunzator fiecaruia
            current_times , current_text = None, ""
            for line in lines:
                #extrag timpul pentru fiecare linie(rand) din subtitrare
                times = re.findall("[0-9]*:[0-9]*:[0-9]*,[0-9]*", line)
                if times != []:
                    current_times = list(map(convert_time, times))
                    #extrag timpul din subtitrare(in secunde)
                elif line == '\n':
                    #salvez intr-o lista text-ul si timpul alocat pentru fiecare in parte
                    times_texts.append((current_times, current_text))
                    current_times, current_text = None, ""
                elif current_times is not None:
                    current_text = current_text + line.replace("\n"," ")

            #salvez timpii alocati pentru fiecare cuvant in parte
            cuts = list(list(find_word(word,times_texts)) for word in words)

            #decupez videoclipul conform timpilor calculati si dupa concatenez rezultatul
            self.result = concatenate([self.clip.subclip(start, end)
                            for (i) in range(len(cuts))
                            for (start,end) in cuts[i]]) 
                        
            #salvez videoclipul
            self.result.to_videofile(output) 

            """
                Metoda "find sequence" realizeaza decupari automate multiple asupra obiectului de tip
                fisier video, aceste decupari realizandu-se pe baza unei liste de cuvite care este orimita ca parametru.
                Practic aceasta functie extrage din videoclip doar secventele in care apar acele cuvinte, adica secventele
                in care personajele rostesc cuvintele cheie care se regasesc in lista primita ca parametru. 

                Functia primeste ca paramerii obiectul de tip video, asupra caruia se va efectua procesul de decupare automata
                (prin termenul "self"), lista de cuvinte cu ajutorul carora sa se efectueze decuparea automata, fisierul
                in care se gaseste subtitrarea, si numele fisierului destinatie.

                Din fisierul de subtitrare se extrage fiecare rand, care contine atat textul aferent randului cat si timpul
                asociat acestuia.

                Din lista de mai sus se extrage timpul. Dupa, trimit ca parametru in functia "find_word" cuvantul cheie si
                lista ce contine textul din fisierul de subtitrare si timpul aferent acestuia.

                Calculez timpul alocat cuvantelor cheie, pentru fiecare cuvant in parte si il returnez sub forma de lista.

                In cele din urma realizez decuparea automata pe baza listei returnate de functia "find_word" si dupa aceea
                salvez in membrul "result" al clasei "Movie" concatenarea videoclipurilor rezultate in urma decuparii
                multiple.

                Astfel se obtine rezultatul dorit.
            """

        except:
            print("Something went wrong with find_sequence method")



def convert_time(timestring):
    try:
        """ Convertesc stringul in secunde(mai exact extrag timpul aferent stringului respectiv) """
        nums = list(map(float, re.findall(r'\d+', timestring)))
        return 3600*nums[0] + 60*nums[1] + nums[2] + nums[3]/1000
    except:
            print("Something went wrong with convert_time function")


def find_word(word,times_texts, padding=.05):
    try:
        """ 
            Functia "find_word" cauta cuvantul dorit in textul subtitrarii si tot odata calculeaza
            timpul corespunzator pentru cuvantul primit ca parametru.

            Rezultatul functiei este reprezentat de doua constante, t1 si t2, unde t1 reprezinta timpul
            de start al cuvantului si t2 timpul de stop al cuvantului.
        """
        matches = [re.search(word, text)
                   for (t,text) in times_texts]

        return [(t1 + m.start()*(t2-t1)/len(text) - padding,
                t1 + m.end()*(t2-t1)/len(text) + padding)
                for m,((t1,t2),text) in zip(matches,times_texts)
                if (m is not None)]
    except:
            print("Something went wrong with find_word function")

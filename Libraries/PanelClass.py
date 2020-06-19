from MovieClass import Movie
import re

path = "C:/Users/rober/Desktop/Workspace/Proiect AM/Proiect/Out_folder/" 
obj_list = []
width_list = []

class Panel:
    #def __init__(self,url):
        #self.url = url
        #self.object = Movie(url)
        #self.name = url.split("\\")
        
    
    def cut(self,url_list,time_list):
        try:
            if len(url_list) > 0 and len(time_list) == 2 :
                movie = Movie(url_list[0])
                name = url_list[0].split("/")
                save_path = path
                save_path = save_path + name[-1]
                temp1 = time_list[0]
                temp2 = time_list[1]
                temp1 = temp1.split(":")
                temp2 = temp2.split(":")
                t1 = 3600*int(temp1[0]) + 60*int(temp1[1]) + int(temp1[2])
                t2 = 3600*int(temp2[0]) + 60*int(temp2[1]) + int(temp2[2])
                if t1 < t2:
                    movie.cut(t1,t2,save_path)
                else:
                    print("Cei doi parametrii au fost introdusi in ordine inversa sau sunt egali!!!")

                return save_path

            else:
                print("The list is empty")
        except:
            print("Something went wrong with cut method from Panel class")

    
    def concat(self,url_list):
        try:
            if len(url_list) > 0 :
                movie = Movie(url_list[0])
                name = url_list[0].split("/")
                save_path = path
                save_path = save_path + name[-1]
                
                for i in range(1,len(url_list)):
                    obj = Movie(url_list[i])
                    obj_list.append(obj.clip)
                    w_dim = obj.clip.size
                    width_list.append(w_dim[1])

                min_resolution = min(width_list)
                m_rez = movie.clip.size
                if m_rez[1] != min_resolution:
                    if m_rez[1] < min_resolution:
                        min_resolution = m_rez[1]
                    else:
                        movie.clip = movie.clip.resize(height = min_resolution)
                print(min_resolution)
                value = False
                if len(width_list) > 0 :
                    value = all(i == width_list[0] for i in width_list)

                    save_path = path
                    save_path = save_path + name[-1]

                    if value == True:
                        movie.concat(save_path,*obj_list)
                    else:
                        for element,i in zip(width_list,range(len(width_list))):
                            if element != min_resolution:
                                obj_list[i] = obj_list[i].resize(height = min_resolution)

                        movie.concat(save_path,*obj_list)

                    return save_path

                else:
                    print("Nu ati introdus o lista valida de fisiere video")

            else:
                print("Nu ati introdus o lista valida de fisiere video")

        except:
            print("Something went wrong with concat method from Panel class")

    
    def video_resize(self,url_list,resolution):
        try:
            if len(url_list) > 0:
                movie = Movie(url_list[0])
                name = url_list[0].split("/")
        
                dim = movie.clip.size
                print(dim)
                if resolution < dim[1]:
                    save_path = path
                    save_path = save_path + name[-1]
                    movie.video_resize(resolution,save_path)

                    return save_path

                else:
                    print("Valoarea pe care ati introdus-o este mai mare sau egala cu rezolutia actuala a videoclipului")
                    print("Va rugam sa introduceti o valoare strict mai mica decat rezolutia videoclipului")

            else:
                print("The list is empty")
        except:
            print("Something went wrong with video_resize method from Panel class")


    def video_mirroring(self,url_list):
        try:
            if len(url_list) > 0:
                movie = Movie(url_list[0])
                name = url_list[0].split("/")
                save_path = path
                save_path = save_path + name[-1]
                movie.video_mirroring(save_path)

                return save_path

            else:
                print("The list is empty")
        except:
            print("Something went wrong with video_mirroring method from Panel class")


    def sound_replace(self,url_list,audio_file,mode):
        try:
            if len(url_list) > 0 :
                movie = Movie(url_list[0])
                name = url_list[0].split("/")
                save_path = path
                save_path = save_path + name[-1]
                movie.sound_replace(audio_file,save_path,mode)

                return save_path

            else:
                print("The list is empty")
        except:
            print("Something went wrong with sound_replace method from Panel class")


    def get_frame(self,url_list,time,extension):
        try:
            if len(url_list) > 0 :
                movie = Movie(url_list[0])
                name = url_list[0].split("/")
                name2 = name[-1]
                name2 = name2.split(".")
                save_path = path
                save_path = save_path + name2[0] + extension
                movie.get_frame(time,save_path)

                return save_path

            else:
                print("The list is empty")
        except:
            print("Something went wrong with get_frame method from Panel class")


    def add_subtitle(self,url_list,subtitle_file):
        try:
            if len(url_list) > 0 :
                movie = Movie(url_list[0])
                name = url_list[0].split("/")
                save_path = path
                save_path = save_path + name[-1]
                movie.add_subtitle(subtitle_file,save_path)

                return save_path

            else:
                print("The list is empty")
        except:
            print("Something went wrong with add_subtitle method from Panel class")


    def find_sequence(self,url_list,words,subtitle_file,mode):
        try:
            if len(url_list) > 0 and len(words) > 0:
                if mode == "clasic":
                    movie = Movie(url_list[0])
                    name = url_list[0].split("/")
                    save_path = path
                    save_path = save_path + name[-1]
                    movie.find_sequence(words,subtitle_file,save_path)

                    return save_path

                if mode == "custom":
                    if len(words)==2:
                        movie = Movie(url_list[0])
                        name = url_list[0].split("/")
                        save_path = path
                        save_path = save_path + name[-1]

                        try:
                            with open(subtitle_file) as f:
                                lines = f.readlines()
                                #deschid fisierul de subtitrare si salvez continutul in variabila lines
                        except:
                            print("Something went wrong with find_sequence method(open file)")

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

                        w1_t = list(find_word(words[0],times_texts))
                        w2_t = list(find_word(words[1],times_texts))
        
                        custom_rez = movie.clip.subclip(w1_t[0][0],w2_t[0][1])
                        custom_rez.write_videofile(save_path)

                        return save_path

                    else:
                        print("Ati introdus prea multe/putine cuvinte. Pentru modul custom trebuie sa introduceti 2 cuvinte!")

                else:
                    print("Nu ati introdus un mod valid. Introduceti clasic sau custom!")

            else:
                print("The list is empty")
        except:
            print("Something went wrong with find_sequence method from Panel class")

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


from MovieClass import Movie
import re
import os
import FoldersConfig
import shutil
path = FoldersConfig.tmpDir.split("\\")
path = "/".join(path)
#path ="C:/MY FILES/Proiect_AM/VideoEditor/VideoEditor/tmp/"
obj_list = []
width_list =[]



class Panel():
    def __init__(self,*args, **kwargs):
        self.test = -1


    def concat(self,url_list):
        try:
            if len(url_list) > 0 :
                movie = Movie(url_list[0])
                name = url_list[0].split("/")
                save_path = path
                save_path = save_path + name[-1]

                newName = name[-1].split('.')
                newName2 = newName[0].split("_edit_")
                try:
                    nr = int(newName2[1])
                    nr = nr + 1
                    nr = str(nr)
                except:
                    nr = "0"
                newSavePath = path + newName2[0] + "_edit_" + nr +"."+ newName[1]
                print("NEW PATH:" + newSavePath)
                save_path = newSavePath

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
                    save_path = newSavePath
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
            return url_list[0]

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

                newName = name[-1].split('.')
                newName2 = newName[0].split("_edit_")
                try:
                    nr = int(newName2[1])
                    nr = nr + 1
                    nr = str(nr)
                except:
                    nr = "0"
                newSavePath = path + newName2[0] + "_edit_" + nr +"."+ newName[1]
                print("NEW PATH:" + newSavePath)
                if t1 < t2:
                    movie.cut(t1,t2,newSavePath)
                else:
                    print("Cei doi parametrii au fost introdusi in ordine inversa sau sunt egali!!!")

                #return save_path
                return newSavePath
            else:
                print("The list is empty")
        except:
            print("Something went wrong with cut method from Panel class")
            return url_list[0]

    def video_resize(self,url_list,resolution):
        try:
            if len(url_list) > 0:
                movie = Movie(url_list[0])
                name = url_list[0].split("/")


                dim = movie.clip.size
                print(dim)
                if int(resolution) < dim[1]:
                    print("If?")
                    save_path = path
                    save_path = save_path + name[-1]
                    newName = name[-1].split('.')
                    newName2 = newName[0].split("_edit_")
                    try:
                        nr = int(newName2[1])
                        nr = nr + 1
                        nr = str(nr)
                    except:
                        nr = "0"
                    newSavePath = path + newName2[0] + "_edit_" + nr +"."+ newName[1]
                    print("NEW PATH:" + newSavePath)
                    save_path = newSavePath

                    resolution = int(resolution)
                    try:
                        movie.video_resize(resolution,save_path)
                    except:
                        return url_list[0]
                    return save_path

                else:
                    print("Valoarea pe care ati introdus-o este mai mare sau egala cu rezolutia actuala a videoclipului")
                    print("Va rugam sa introduceti o valoare strict mai mica decat rezolutia videoclipului")
                    return url_list[0]

            else:
                print("The list is empty")
                return url_list[0]
        except:
            print("Something went wrong with video_resize method from Panel class")
            return url_list[0]

    def video_mirroring(self,url_list):
        try:
            if len(url_list) > 0:
                movie = Movie(url_list[0])
                name = url_list[0].split("/")
                save_path = path
                save_path = save_path + name[-1]
                newName = name[-1].split('.')
                newName2 = newName[0].split("_edit_")
                try:
                    nr = int(newName2[1])
                    nr = nr + 1
                    nr = str(nr)
                except:
                    nr = "0"
                newSavePath = path + newName2[0] + "_edit_" + nr +"."+ newName[1]
                print("NEW PATH:" + newSavePath)
                save_path = newSavePath
                movie.video_mirroring(save_path)
                return save_path

            else:
                print("The list is empty")
        except:
            print("Something went wrong with video_mirroring method from Panel class")
            return url_list[0]

    def soundReplace(self,url_list,audio_file,mode):
        try:
            if len(url_list) > 0 :
                movie = Movie(url_list[0])
                name = url_list[0].split("/")
                save_path = path
                save_path = save_path + name[-1]
                newName = name[-1].split('.')
                newName2 = newName[0].split("_edit_")
                try:
                    nr = int(newName2[1])
                    nr = nr + 1
                    nr = str(nr)
                except:
                    nr = "0"
                newSavePath = path + newName2[0] + "_edit_" + nr +"."+ newName[1]
                print("NEW PATH:" + newSavePath)
                save_path = newSavePath
                movie.sound_replace(audio_file,save_path,mode)

                return save_path

            else:
                print("The list is empty")
                return url_list[0]
        except:
            print("Something went wrong with sound_replace method from Panel class")
            return url_list[0]

    def getFrame(self,url_list,time):

        try:
            if len(url_list) > 0 :
                movie = Movie(url_list[0])
                name = url_list[0].split("/")
                name2 = name[-1]
                name2 = name2.split(".")
                save_path = path
                save_path = save_path + name2[0] + ".jpg"
                movie.get_frame(time,save_path)

                return save_path

            else:
                print("The list is empty")
        except:
            print("Something went wrong with get_frame method from Panel class")

    def addSubtitles(self,url_list,subtitle_file):
        try:
            if len(url_list) > 0 :
                movie = Movie(url_list[0])
                name = url_list[0].split("/")
                save_path = path
                save_path = save_path + name[-1]
                newName = name[-1].split('.')
                newName2 = newName[0].split("_edit_")
                try:
                    nr = int(newName2[1])
                    nr = nr + 1
                    nr = str(nr)
                except:
                    nr = "0"
                newSavePath = path + newName2[0] + "_edit_" + nr +"."+ newName[1]
                print("NEW PATH:" + newSavePath)
                save_path = newSavePath
                movie.add_subtitle(subtitle_file,save_path)

                return save_path

            else:
                print("The list is empty")
        except:
            print("Something went wrong with add_subtitle method from Panel class")
            return url_list[0]

    def find_sequence(self,url_list,words,subtitle_file,mode):
        try:
            if len(url_list) > 0 and len(words) > 0:
                if mode == "Clasic":
                    movie = Movie(url_list[0])
                    name = url_list[0].split("/")
                    save_path = path
                    save_path = save_path + name[-1]
                    newName = name[-1].split('.')
                    newName2 = newName[0].split("_edit_")
                    try:
                        nr = int(newName2[1])
                        nr = nr + 1
                        nr = str(nr)
                    except:
                        nr = "0"
                    newSavePath = path + newName2[0] + "_edit_" + nr +"."+ newName[1]
                    print("NEW PATH:" + newSavePath)
                    save_path = newSavePath
                    movie.find_sequence(words,subtitle_file,save_path)
                    return save_path

                if mode == "Custom":
                    if len(words)==2:
                        movie = Movie(url_list[0])
                        name = url_list[0].split("/")
                        save_path = path
                        save_path = save_path + name[-1]
                        newName = name[-1].split('.')
                        newName2 = newName[0].split("_edit_")
                        try:
                            nr = int(newName2[1])
                            nr = nr + 1
                            nr = str(nr)
                        except:
                            nr = "0"
                        newSavePath = path + newName2[0] + "_edit_" + nr +"."+ newName[1]
                        print("NEW PATH:" + newSavePath)
                        save_path = newSavePath

                        try:
                            with open(subtitle_file) as f:
                                lines = f.readlines()
                                #deschid fisierul de subtitrare si salvez continutul in variabila lines
                        except:
                            print("Something went wrong with find_sequence method(open file)")
                            return url_list[0]

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
            return url_list[0]








def convert_time(timestring):
    try:
        """ Convertesc stringul in secunde(mai exact extrag timpul aferent stringului respectiv) """
        nums = list(map(float, re.findall(r'\d+', timestring)))
        return 3600*nums[0] + 60*nums[1] + nums[2] + nums[3]/1000
    except:
            print("Something went wrong with convert_time function")

def find_word(word,times_texts, padding=.05):

    """
        Functia "find_word" cauta cuvantul dorit in textul subtitrarii si tot odata calculeaza
        timpul corespunzator pentru cuvantul primit ca parametru.

        Rezultatul functiei este reprezentat de doua constante, t1 si t2, unde t1 reprezinta timpul
        de start al cuvantului si t2 timpul de stop al cuvantului.
    """
    try:
        matches = [re.search(word, text)
                for (t,text) in times_texts]

        return [(t1 + m.start()*(t2-t1)/len(text) - padding,
            t1 + m.end()*(t2-t1)/len(text) + padding)
            for m,((t1,t2),text) in zip(matches,times_texts)
            if (m is not None)]
    except:
        print("Something went wrong with find_word function")

from Class_V1 import Movie

path = "C:/MY FILES/Proiect_AM/VideoEditor/VideoEditor/tmp/"
obj_list = []
width_list = []

class Panel():
    def __init__(self, *args, **kwargs):
        self.test = -1


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
    def cut(self,videoList,t1,t2):
        return videoList[0]
    def video_resize(self,videoList,res):
        print(res)
        return videoList[0]

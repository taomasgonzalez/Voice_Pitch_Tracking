from scipy.io import wavfile as wave
import scipy.signal as sig
import matplotlib.pyplot as plt

BUFFER_SIZE = 10E4
MONO = 1
STEREO = 2


class GraphSpectrogram():
    def __init__(self,file_name):
        self.file_name= file_name
        #Variables por default
        self.window = 'hann'
        self.nperseg = 1024
        self.nfft=None
        self.noverlap=512
        self.window_dict = dict([
            ('1','hann'),
            ('2','flattop'),
            ('3','boxcar'),
            ('4','triang'),
            ('5','bartlett'),
            ('6','parzen')
            ])

        self.ShowSpectrogram()
    def GetSpectrogram(self):
         file_name = self.file_name
         window_u = self.window
         nperseg_u = self.nperseg
         nfft_u = self.nfft
         noverlap_u = self.noverlap

         f_s, file = wave.read(file_name)
         data_size = len( file.shape )
         if data_size == MONO:
             f,t,spec= sig.spectrogram(file,fs=f_s,window=window_u,nperseg=nperseg_u,noverlap=noverlap_u,nfft=nfft_u)
         elif data_size == STEREO:
            f_1,t_1,spec_1 =sig.spectrogram(file[:,0],fs=f_s,window=window_u,nperseg=nperseg_u,noverlap=noverlap_u,nfft=nfft_u)
            f_2,t_2,spec_2 =sig.spectrogram(file[:,1],fs=f_s,window=window_u,nperseg=nperseg_u,noverlap=noverlap_u,nfft=nfft_u)
            f = f_1
            t = t_1
            spec = 0.5*(spec_1+spec_2)
         else:
             print("Error")
             return

         plt.pcolormesh(t, f, spec)
         plt.title("Espectrograma de "+file_name)
         plt.xlabel("t(seg)")
         plt.ylabel("f(Hz)")
         plt.ylim(top=f[-1])
         plt.xlim(right=t[-1])
         plt.show()

    def ShowSpectrogram(self):
        file_name = self.file_name
        print("\nIngrese 'y' en caso afrimativo, en caso contrario ingrese cualquier otra tecla.")
        user_string = input("Desea ver el espectrograma del audio sintetizado?\n")
        if( (user_string == 'y') or (user_string == 'Y') ):
            param_string = input("Desea configurar los parametros del espectrograma? (En caso contrario se usaran valores por default)\n")
            if( (param_string == 'y') or (param_string == 'Y') ):
                self.GetAndValidateParams()
            self.GetSpectrogram()
    def GetAndValidateParams(self):
        valid = False
        while not valid: #Valido la ventana elegida
            print("Ingresar el numero previo al nombre de la ventana que desea")
            inp= input("Eliga el tipo de ventana que quiere:\n 1)Hann\t 2)Flat top\t 3)Square\n 4)Triangular\t 5)Bartlett\t 6)Parzen\n")
            if inp in self.window_dict:
                self.window = self.window_dict[inp]
                valid=True
            else:
                print("La opcion elegida es invalida,ingrese unicamente alguno de los numeros provistos") 
        valid=False
        while not valid: #Valido nperseg
            length = input("Por favor especificar el largo de cada ventana (Se recomienda un largo menor a 2210)\n")
            validiy_str = self.IsValidNumber(length)
            if(validiy_str == 'Ok'):
                valid= True
                self.nperseg = int(float(length))
            else:
                print(validiy_str)
        valid = False
        while not valid: #Valido nfft
            length = input("Por favor especificar el numero de muestras de cada FFT (Se recomienda un numero igual o mayor al ingresado previamente)\n")
            validiy_str = self.IsValidNumber(length)
            if(validiy_str == 'Ok'):
                valid= True
                self.nfft = int(length)
            else:
                print(validiy_str)
        valid = False
        while not valid: #Valido noverlap
            overlap_str = input("Por favor especificar el numero de muestras que se superponen de cada ventana\n")
            validiy_str = self.IsValidNumber(length)
            if(validiy_str == 'Ok'):
                if int(overlap_str)< self.nperseg:
                    self.noverlap = int(overlap_str)
                    valid = True
                else:
                    print("Este numero debe ser menor que el largo de la ventana especificado previamente\n")
            else:
                print(validiy_str)




    #funciones auxiliares
    def isfloat(self,value):
      try:
        float(value)
        return True
      except ValueError:
        return False

    def IsValidNumber(self,arg):
        if( self.isfloat(arg)): #valido el argumento
            arg_f=float(arg)
            if(arg_f<=0):
                return ( "El numero ingresado debe ser positivo\n")
            elif (arg_f==float("inf"))or(arg_f>=10e9):
                return ("El numero ingresado debe tener un valor finito\n")

        else:
            return ("Error de sintaxis")

        return "Ok" #El numero parece ser valido


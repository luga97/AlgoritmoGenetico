# Se importan las librería necesarias
import numpy as np
import math as mt



class Genetico():
    def __init__(self,tam,min,max,tol):
        
        self.tam=tam        # Tamaño de la población
        
        self.Xmin=min       # Minimo de X
        self.Xmax=max       # Maximo de X
        self.Ymin=min       # Minimo de Y
        self.Ymax=max       # Maximo de Y

        self.tol=tol                                            # Tolerancia

        self.long_total = self.longitudX()+self.longitudY()      #Longitud total de los cromosomas
        #print("longitud total: ",self.long_total)
        self.poblacion=self.primera_poblacion()                  # Se crea la población inicial
        print("poblacion inicial: \n",self.poblacion)
        
        self.pro_cruce=0.80
        self.pro_mutar=0.10
        #self.aptitud=self.Aptitud()                # Se determina la aptitud de los individuos de la Población con el método Aptitud
    
    def longitudX(self):
        tam = mt.log2(self.Xmax+(self.Xmax-self.Xmin)/self.tol)
        tam = mt.ceil(tam)
        #print("longitud en X: ",tam)
        return tam

    def longitudY(self):
        tam = mt.log2(self.Xmax+(self.Ymax-self.Ymin)/self.tol)
        tam = mt.ceil(tam)
        #print("longitud en Y: ",tam)
        return tam
    
    def aptitud(self):
        #return -(x**2-0.3*np.cos(4*np.pi*x)+0.3)+30
        self.apt = 20+self.X**2+self.Y**2-10*(np.cos(2*np.pi*self.Y)+np.cos(2*np.pi*self.X))
        self.apt = 1000/(self.apt+100)
        #self.apt = 50-self.X**2-self.Y**2
        return self.apt
    
    def primera_poblacion(self): # Método para generar la población inicial
        return np.random.randint(0,2,[self.tam,self.long_total])

    def cruzar(self):
        for i in range(0,self.tam):
            #print("\n------------- RECORRIENDO POBLACION | CROMOSOMA {} -------------\n".format(i))
            cruce = np.random.rand()        #valor random que indica si se realizara el cruce
            #print("valor random de cruce: ",cruce)
            #Si el valor random es menor que la probabilidad de cruce cruzamos
            if cruce<self.pro_cruce:
                j=np.random.randint(1,self.tam-1)
                #print("el cromosoma: {} \nse cruzara con el cromosoma: {}".format(self.poblacion[i,],self.poblacion[j,]))
                while i==j:
                    j=np.random.randint(1,self.tam-1)
                #aqui se genera el cruce    
                punto=np.random.randint(1,self.long_total)          # Se genera un punto de cruce
                #print("y se cruzaran en el punto: ",punto)
                #variable auxilar para la segunda parte del primer array, si no se usa el comportamiento no es el esperado
                aux = np.copy(self.poblacion[i,punto:])
                self.poblacion[i,]=np.concatenate((self.poblacion[i,:punto],self.poblacion[j,punto:]),axis=0)
                self.poblacion[j,]=np.concatenate((self.poblacion[j,:punto],aux),axis=0)
                #print("cromosoma i mutado: {}".format(self.poblacion[i,]))
                #print("cromosoma j mutado: {}".format(self.poblacion[j,]))
    def mutar(self):
        #print("\n------------- MUTACION  -------------\n")
        
        for i in range(self.tam):
            mutar = np.random.rand()
            #print("PROBABILIDA DE MUTAR DEL CROMOSOMA NRO {}: {}".format(i,round(mutar,3)))
            if mutar<self.pro_mutar:
                point=np.random.randint(0,self.long_total)  
                #print("El cromosoma {} muto en el punto {}".format(i,point))

                if self.poblacion[i,point]==0:
                    self.poblacion[i,point]=1
                else:
                    self.poblacion[i,point]=0
                #print(self.poblacion[:])
            
    def seleccion(self):
        print("viejas aptitudes: ",self.aptitud())
        #elitismo    
        indmax=np.argmax(self.aptitud())
        #print(indmax)
        self.poblacion[0]=self.poblacion[indmax]
        # Se realiza la seleccion por rueda de ruleta
        apt=abs(np.cumsum(self.aptitud())/np.sum(self.aptitud()))
        
        #aux=P.aptitud/sum(P.aptitud)
        for i in range(1,self.tam):
            r=np.random.rand()
            self.poblacion[i,:]=self.poblacion[np.argmax(apt>r),:]
        self.decodificar()
        print("nueva aptitudes: ",self.aptitud())
    
    def decodificar(self):
        self.X= self.Y =np.array([])
        for i in range(self.tam):
            pc = self.longitudX()
            x,y = self.binToDec(self.poblacion[i,:pc]), self.binToDec(self.poblacion[i,pc:])
            x,y = self.transformar(x,y)
            #sprint("(x,y) = ({},{})".format(x,y))
            
            self.X = np.append(self.X,x)
            self.Y = np.append(self.Y,y)
    
    def binToDec(self,bin):
        aux = ''.join(map(lambda bin_array: str(int(bin_array)), bin))
        return int(aux,2)
    
    def transformar(self,x,y):
        valor=x
        vtx=self.Xmin+valor*(self.Xmax-self.Xmin)/(2**(self.longitudX())-1)
        x= round(vtx,2)
        valor=y
        vty=self.Ymin+valor*(self.Ymax-self.Ymin)/(2**(self.longitudY())-1)
        y = round(vty,2)
        return x,y
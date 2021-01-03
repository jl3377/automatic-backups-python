#!/usr/bin/env python3

# Del Módulo "ftplib" importamos la clase "FTP" 
import os
import sys
import json
import ftplib
import socket
import subprocess
from ftplib import FTP_TLS
from datetime import datetime

class Backup( object ):

  def __init__(self, name):
    """Read config file, make connecction and make backup."""

    self.name = str(name) # name backup

    # set [PID] from process
    self.pid = "["+str(os.getpid())+"]"         

    # leer el fichero de configuración
    if self.config():
      # declarar la variable self.ftp que usaremos en las funciones.
      self.ftp = FTP_TLS()
      # check files and directories that need backup
      if self.check_files_and_dirs():
        self.log("ficheros copiados")

      # conexión al ftp      
      if self.conectar() == True:    
        # carga de ficheros
        self.cargar_ficheros()    
        #pass

  def config(self):
    """cargar ficheros de configuración """

    try:
      with open("./conf/config.py", "r") as conf:
        self.data = json.load(conf)                      
        return self.data
    except:      
      self.log("ERROR: File config not found.")

  def check_files_and_dirs(self):
    """check files and directories that need backup """
    
    self.log("Reading Backup info from: "+self.name)
    self.log("Reading files and directories from config file ")
    
    if self.data[self.name]["backup"]["files"] != "" or self.data[self.name]["backup"]["directories"] != "":
      self.files_to_backup = self.data[self.name]['backup']["files"].split(",")    
      self.directories_to_backup = self.data[self.name]['backup']["directories"].split(",")
      
      # preparing files   
      if self.files_to_backup != "":
        files_to_process = ""
        for file in self.files_to_backup:
          files_to_process += str(file)      
        self.log("Preparando ficheros: "+files_to_process)

      # preparing directories      
      if self.directories_to_backup != "":
        directories_to_process = ""      
        for directory in self.directories_to_backup:
          directories_to_process += str(directory)        
        self.log("Preparando directorios: "+directories_to_process)  

      # backup files and directories
      self.backup_file = str(datetime.now().strftime("%Y-%m-%d_%H_%M_%S"))+"_"+self.name+".tar.gz"                        
      cmd = "tar -czf "+ "tmp/"+str(self.backup_file)+ " "+files_to_process+ " "+directories_to_process
      subprocess.Popen(cmd, shell=True, close_fds=False)      
      
      return True
    return False
  
  def conectar(self):
    """conexión al FTP"""

    try:
      self.log("Conectando a ... " + self.data[self.name]["ftp"])
      self.ftp.connect(self.data[self.name]["ftp"])
      self.ftp.login(self.data[self.name]["user"], self.data[self.name]["passwd"])     
      self.log("Conexión establecida.")
      self.log("Comprobando datos de acceso ...")      
      self.log("Usuario "+self.data[self.name]["user"]+" aceptado.")                 
      return True
    except ftplib.error_perm as error:      
      self.log("ERROR:"+str(error))       
    except (socket.error,socket.gaierror) as error:
      self.log("ERROR: no se pudo conectar al FTP "+self.data[self.name]["ftp"])    
    except:      
      self.log("ERROR: Error indeterminado")    
    return False
  
  def cargar_ficheros(self):
    """carga de ficheros al FTP """

    tmp_dir = self.data[self.name]["tmp_dir"]
    backups_dir = self.data[self.name]["backup_dir"]
    try:
      with open(tmp_dir+self.backup_file, "rb") as file:       
        self.ftp.cwd(backups_dir)
        self.ftp.storbinary('STOR '+str(self.backup_file), file)
        self.log("Cargando fichero ..."+self.backup_file)    
        #self.ftp.storlines('STOR '+str(self.backup_file), file)
        self.log("Cerrando la conexión con el FTP.")    
        self.ftp.close()

        #remove file from tmp directory
        os.remove(tmp_dir+self.backup_file)
    except:
      self.log("ERROR: No se pudieron cargar los ficheros.")        
      
  def log(self, msg):
    """escribir mensajes en fichero de log"""

    self.fecha = "["+str(datetime.now().strftime("%d/%m/%Y %H:%M:%S"))+"]"
    with open(self.data[self.name]["log_dir"], "a+") as file:
      file.write(self.fecha+" "+self.pid+" "+str(msg)+"\n")

  def debug(self):
    pass


b = Backup("artegrafico.net")  
# https://python.hotexamples.com/examples/ftplib/FTP/pwd/python-ftp-pwd-method-examples.html

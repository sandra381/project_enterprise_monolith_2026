# Onboarding Log - DevEx Audit

Este onboarding log documenta la experiencia inicial de configuración y ejecución del proyecto Spring PetClinic, con el fin de identificar fricciones y oportunidades de mejora en la experiencia del desarrollador.

## Entorno Usado

-Sistema operativo: Windows  
-Terminal: PowerShell  
-Java Instalado: Java 22  
-Proyecto: Spring PetClinic  

## Proceso de configuración inicial

-Revisar el repositorio de github para comprender su estructura.  
-Se identificó el archivo README, el cual contenía la descripción de distintas formas de ejecutar el proyecto.  
-En base a esta información se eligió la opción de ejecutar el programa de manera local.  
-Se clonó el repositorio del proyecto desde Github en la computadora local.  
-Una vez clonado, se accedió a la carpeta spring-petclinic del proyecto utilizando la terminal.  
-En el README se presentan comandos orientados principalmente a entornos Linux/macOS como ./mvnw spring-boot:run , sin embargo el entorno utilizado fue Windows por lo que se adaptó el comando correspondiente para ejecutarlo en la PowerShell.  
-En base a esta información se logró la ejecución del proyecto sin la necesidad de instalar las dependencias necesarias, ya que se utilizó Maven.  
-Una vez iniciado el proyecto, se accedió a la aplicación desde el navegador mediante http://localhost:8080, mostrando correctamente la página principal.

## Puntos de fricción y oportunidades de mejora

-Al trabajar por primera vez con el proyecto, se pudo ejecutar el sistema sin mayores complicaciones; sin embargo, la cantidad de archivos y carpetas resulta difícil de entender para alguien que se incorpora por primera vez.
-El proyecto no cuenta con una descripción básica que explique qué hace cada carpeta o archivo principal, lo que dificulta la comprensión inicial del funcionamiento del sistema y hace necesario explorar el proyecto de manera manual.
-La primera ejecución del proyecto tardó aproximadamente 10.597 segundos en iniciar, tiempo durante el cual se mostraron varios mensajes en la consola mientras se descargaban dependencias y se realizaba la configuración inicial.
-Este comportamiento puede generar dudas en desarrolladores nuevos, ya que no es del todo claro en qué momento el sistema terminó de cargar correctamente y está listo para usarse.


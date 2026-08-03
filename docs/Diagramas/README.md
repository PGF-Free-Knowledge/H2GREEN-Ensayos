# H2GREEN - Diagramas del Proyecto

Esta carpeta reúne la documentación gráfica oficial del proyecto **H2GREEN**, desarrollada para describir la arquitectura general del sistema, los lazos de control implementados y la secuencia operacional del prototipo de ensayo automatizado para evaluación de materiales en atmósferas asociadas al hidrógeno.

---

# Índice

1. Arquitectura General del Sistema
2. Lazo de Control de Presión
3. Lazo de Control de Temperatura
4. Lazo de Control de Desplazamiento
5. Lazo de Fuerza y Desplazamiento
6. Secuencia Completa del Proceso

---

# 01. Arquitectura General del Sistema

![Arquitectura General](01_Arquitectura_General_del_Sistema.png)

## Objetivo

Presentar la arquitectura general del sistema, mostrando la interacción entre el Dashboard H2GREEN, Arduino Mega Maestro, Arduino esclavos, cámara Basler y dispositivos de campo.

## Descripción funcional

La arquitectura general del sistema H2GREEN está basada en una estructura distribuida de supervisión y control, donde el Dashboard desarrollado en Python actúa como interfaz principal del operador y el Arduino Mega funciona como controlador maestro del sistema.

El Dashboard permite configurar el ensayo, supervisar el estado de operación, registrar las variables del proceso, visualizar gráficos en tiempo real y coordinar la ejecución automática de la secuencia de ensayo.

El Arduino Mega Maestro centraliza la comunicación con los cuatro Arduino esclavos especializados, siendo responsable de distribuir las órdenes recibidas desde el Dashboard, sincronizar la ejecución de cada módulo y consolidar la información proveniente de los dispositivos de adquisición.

Cada Arduino esclavo ejecuta una función específica dentro del sistema:

- Arduino Presión: adquisición de presión y control de electroválvulas.
- Arduino Fuerza: adquisición de la señal proveniente de la celda de carga mediante el módulo HX711.
- Arduino Temperatura: adquisición de temperatura y control futuro del sistema térmico mediante un controlador PID.
- Arduino Velocidad: control del driver SH-1108 y del motor paso a paso responsable del desplazamiento del ensayo.

La cámara Basler constituye el sistema de visión artificial del proyecto y será utilizada para la medición precisa del desplazamiento de la probeta, permitiendo complementar las mediciones obtenidas mediante la instrumentación electrónica.

Toda la información adquirida por los módulos es enviada al Dashboard Python para su almacenamiento, visualización y posterior generación de resultados del ensayo.

## Flujo de operación

1. El operador inicia el Dashboard H2GREEN desde el computador de supervisión.

2. El Dashboard inicializa la interfaz gráfica, carga la configuración del sistema y prepara la comunicación serial.

3. Python establece la comunicación con el Arduino Mega Maestro.

4. El Arduino Mega verifica la disponibilidad y comunicación de los cuatro Arduino esclavos:
   - Presión
   - Fuerza
   - Temperatura
   - Velocidad

5. Cada Arduino esclavo inicializa el hardware asociado a su función y comienza la adquisición continua de datos.

6. El Arduino Mega consolida toda la información recibida desde los módulos esclavos y la transmite al Dashboard Python.

7. El Dashboard actualiza en tiempo real los indicadores, gráficos, estados del sistema y registro de variables.

8. Cuando el operador ejecuta una acción desde el Dashboard (por ejemplo, iniciar la secuencia automática o comenzar un ensayo), el comando es enviado al Arduino Mega.

9. El Arduino Mega distribuye las órdenes al Arduino esclavo correspondiente, coordinando la ejecución de cada lazo de control.

10. Durante toda la operación, el Dashboard registra las variables del ensayo, supervisa el estado del sistema y almacena la información para su posterior análisis.

## Implementación relacionada

- [Dashboard H2GREEN](../../python/Dashboards/Dashboard_H2Green_v1.0.py)
- [Arduino Mega Maestro](../../arduino/maestro/Mega_H2Green_v1.0.ino)
- [Arduino Presión](../../arduino/presion/Presion_H2Green_v1.0.ino)
- [Arduino Fuerza](../../arduino/fuerza/Fuerza_H2Green_v1.0.ino)
- [Arduino Temperatura](../../arduino/temperatura/Temperatura_H2Green_v1.0.ino)
- [Arduino Velocidad](../../arduino/velocidad/Velocidad_H2Green_v1.0.ino)

---

# 02. Secuencia Detallada del Lazo de Presión

![Lazo Presión](02_Secuencia_Detallada_Lazo_de_Presion.png)

## Objetivo

Documentar el funcionamiento del lazo de presión, incluyendo purga, presurización, estabilización y control de electroválvulas.

## Descripción funcional

El lazo de control de presión es el encargado de preparar la cámara de ensayo antes de iniciar el ensayo mecánico, controlando la secuencia de purga, presurización, estabilización, exposición y descarga de la presión de forma completamente automática.

El Dashboard Python supervisa continuamente el estado del proceso, mientras que el Arduino Mega coordina el funcionamiento del Arduino esclavo de presión, responsable de la adquisición de las señales provenientes de los transmisores de presión y del accionamiento de las electroválvulas del sistema.

Durante cada etapa, el sistema verifica las condiciones de operación, actualiza el estado del proceso y garantiza que la transición entre etapas se realice únicamente cuando se cumplen las condiciones definidas para el ensayo.

El objetivo principal de este lazo es asegurar que la probeta alcance las condiciones de presión requeridas antes de habilitar el inicio del ensayo mecánico.

## Flujo de operación

1. El operador configura desde el Dashboard Python los parámetros del ensayo, incluyendo la presión objetivo y el tiempo de exposición.

2. Al presionar el botón **AUTO**, el Dashboard envía el comando correspondiente al Arduino Mega Maestro para iniciar la secuencia automática.

3. El Arduino Mega cambia el estado del sistema a **PURGA** y solicita al Arduino esclavo de presión ejecutar la primera etapa del proceso.

4. El Arduino de presión controla las electroválvulas correspondientes para realizar la purga de la cámara, eliminando el aire residual y preparando el sistema para la presurización.

5. Finalizada la purga, el Arduino Mega cambia automáticamente al estado **PRESURIZACIÓN**, ordenando al Arduino de presión iniciar el incremento controlado de la presión.

6. Durante la presurización, el Arduino de presión monitorea continuamente los transmisores PT-01 y PT-02, enviando las mediciones al Arduino Mega.

7. El Arduino Mega transmite las variables al Dashboard Python, donde el operador puede supervisar en tiempo real la evolución de la presión y el estado del sistema.

8. Una vez alcanzada la presión objetivo, el sistema cambia automáticamente al estado **ESTABILIZACIÓN**, verificando que la presión permanezca dentro del rango definido para el ensayo.

9. Cumplida la estabilización, el sistema inicia la etapa de **EXPOSICIÓN**, manteniendo la probeta sometida a la presión establecida durante el tiempo programado.

10. Finalizado el tiempo de exposición, el Dashboard habilita automáticamente el inicio del ensayo mecánico, permitiendo continuar con la secuencia general del sistema.

## Implementación relacionada

- [Dashboard H2GREEN](../../python/Dashboards/Dashboard_H2Green_v1.0.py)
- [Arduino Presión](../../arduino/presion/Presion_H2Green_v1.0.ino)

---

# 03. Secuencia Detallada del Lazo de Temperatura

![Lazo Temperatura](03_Secuencia_Detallada_Lazo_de_Temperatura.png)


## Objetivo

Describir el sistema de control térmico compuesto por sensor de temperatura, Arduino esclavo, SSR y calefactor.

## Descripción funcional

El lazo de control de temperatura tiene como objetivo supervisar y regular la temperatura de la cámara de ensayo durante todo el proceso experimental.

El Arduino esclavo de temperatura realiza la adquisición continua de la temperatura mediante el sensor instalado en la cámara, enviando periódicamente esta información al Arduino Mega Maestro.

El Dashboard Python recibe las mediciones en tiempo real, permitiendo al operador visualizar la evolución de la temperatura y verificar que las condiciones del ensayo permanezcan dentro de los rangos establecidos.

En la versión actual del prototipo, este módulo realiza la adquisición y supervisión de la temperatura. En versiones posteriores incorporará un controlador PID para regular automáticamente el calefactor mediante un relé de estado sólido (SSR), manteniendo la temperatura objetivo durante todo el ensayo.

## Flujo de operación

1. Al iniciar el Dashboard H2GREEN, el Arduino Mega establece comunicación con el Arduino esclavo de temperatura.

2. El Arduino esclavo inicializa el sensor de temperatura y comienza la adquisición continua de las mediciones de la cámara de ensayo.

3. Cada lectura de temperatura es enviada al Arduino Mega Maestro mediante comunicación serial.

4. El Arduino Mega transmite la información al Dashboard Python para su visualización y registro en tiempo real.

5. El Dashboard actualiza continuamente el indicador de temperatura, permitiendo al operador supervisar la condición térmica del ensayo.

6. Durante toda la secuencia automática, la temperatura es monitoreada de forma permanente para verificar que permanezca dentro del rango esperado.

7. En la versión actual del prototipo, el sistema realiza funciones de adquisición y supervisión de temperatura.

8. En una etapa posterior del proyecto, el Arduino esclavo incorporará un controlador PID que actuará sobre un relé de estado sólido (SSR) para regular automáticamente el calefactor de la cámara y mantener la temperatura programada durante todo el ensayo.

## Implementación relacionada

- [Dashboard H2GREEN](../../python/Dashboards/Dashboard_H2Green_v1.0.py)
- [Arduino Temperatura](../../arduino/temperatura/Temperatura_H2Green_v1.0.ino)

---

# 04. Secuencia Detallada del Lazo de Desplazamiento del Motor

![Lazo Desplazamiento](04_Secuencia_Detallada_Lazo_de_Desplazamiento_Motor.png)

## Objetivo

Describir el control del desplazamiento mediante Arduino, driver SH-1108 y motor paso a paso.

## Descripción funcional

El lazo de control de desplazamiento es el encargado de gobernar el movimiento del motor paso a paso que aplica el desplazamiento controlado sobre la probeta durante el ensayo mecánico.

El Dashboard Python permite configurar la velocidad y las condiciones de operación del ensayo, enviando los parámetros correspondientes al Arduino Mega Maestro.

El Arduino Mega coordina el funcionamiento del Arduino esclavo de velocidad, responsable de controlar el driver SH-1108, el cual suministra la potencia necesaria para accionar el motor paso a paso.

El movimiento del motor determina la velocidad de aplicación de la carga mecánica sobre la probeta, asegurando que el ensayo se realice bajo las condiciones establecidas por el operador.

Durante todo el proceso, el Dashboard supervisa el estado del sistema y registra las variables necesarias para el posterior análisis del ensayo.

## Flujo de operación

1. El operador configura desde el Dashboard Python la velocidad de desplazamiento requerida para el ensayo.

2. El Dashboard envía los parámetros de velocidad al Arduino Mega Maestro mediante comunicación serial.

3. El Arduino Mega procesa la información recibida y transmite la orden al Arduino esclavo de velocidad.

4. El Arduino esclavo genera las señales de control STEP y DIR necesarias para el funcionamiento del driver SH-1108.

5. El driver SH-1108 suministra la potencia requerida al motor paso a paso, permitiendo el desplazamiento controlado del sistema mecánico.

6. El motor desplaza la probeta a la velocidad programada por el operador, manteniendo las condiciones definidas para el ensayo.

7. Durante toda la ejecución, el Dashboard supervisa el estado del sistema, registra las variables del ensayo y mantiene sincronizada la operación con los demás lazos de control.

8. En las siguientes versiones del proyecto, este módulo podrá incorporar estrategias adicionales de control para optimizar el movimiento del sistema, supervisar condiciones de operación y mejorar la precisión del ensayo.

## Implementación relacionada

- [Dashboard H2GREEN](../../python/Dashboards/Dashboard_H2Green_v1.0.py)
- [Arduino Velocidad](../../arduino/velocidad/Velocidad_H2Green_v1.0.ino)

---

# 05. Secuencia Detallada del Lazo de Fuerza y Desplazamiento

![Lazo Fuerza](05_Secuencia_Detallada_Lazo_de_Fuerza_y_Desplazamiento.png)

## Objetivo

Describir la adquisición de fuerza mediante la celda de carga y HX711, junto con el desplazamiento obtenido mediante visión artificial usando la cámara Basler.

## Descripción funcional

El lazo de fuerza y desplazamiento es el encargado de adquirir las variables mecánicas principales del ensayo, permitiendo evaluar el comportamiento de la probeta durante la aplicación de carga.

El Arduino esclavo de fuerza adquiere continuamente la señal proveniente de la celda de carga mediante el módulo HX711, transmitiendo las mediciones al Arduino Mega Maestro.

Paralelamente, el desplazamiento de la probeta será obtenido mediante el sistema de visión artificial basado en la cámara Basler, permitiendo determinar el desplazamiento real durante el ensayo.

El Dashboard Python integra ambas variables, sincronizando la información recibida para visualizar en tiempo real las curvas Fuerza–Desplazamiento y generar posteriormente las curvas Esfuerzo–Deformación utilizadas en el análisis del comportamiento mecánico del material.

## Flujo de operación

1. Una vez finalizada la etapa de exposición, el Dashboard H2GREEN habilita el inicio del ensayo mecánico.

2. El Arduino Mega Maestro coordina el inicio simultáneo de la adquisición de fuerza y del control de desplazamiento.

3. El Arduino esclavo de fuerza comienza la lectura continua de la celda de carga mediante el módulo HX711, enviando las mediciones al Arduino Mega.

4. Paralelamente, el sistema registra el desplazamiento aplicado a la probeta y, en las siguientes versiones del proyecto, incorporará la medición directa mediante la cámara Basler y procesamiento de imágenes.

5. El Arduino Mega transmite continuamente las variables de fuerza y desplazamiento al Dashboard Python para su visualización en tiempo real.

6. El Dashboard registra automáticamente todas las mediciones del ensayo en archivos CSV y actualiza las gráficas de Fuerza–Desplazamiento durante la ejecución del ensayo.

7. Al finalizar el ensayo, la información registrada permitirá generar las curvas Esfuerzo–Deformación y realizar el análisis del comportamiento mecánico de la probeta.

8. En futuras versiones, el sistema incorporará la detección automática de rotura, finalizando el ensayo de manera segura cuando se identifique la falla del material.

## Implementación relacionada

- [Dashboard H2GREEN](../../python/Dashboards/Dashboard_H2Green_v1.0.py)
- [Arduino Fuerza](../../arduino/fuerza/Fuerza_H2Green_v1.0.ino)

---

# 06. Secuencia Completa del Proceso

![Secuencia Completa](06_Secuencia_Completa_del_Proceso.png)

## Objetivo

Integrar todos los lazos de control y mostrar la secuencia completa de operación del sistema H2GREEN desde la inicialización hasta la finalización del ensayo.

## Descripción funcional

La secuencia completa del proceso integra todos los lazos de control desarrollados para el proyecto H2GREEN, coordinando el funcionamiento del Dashboard Python, Arduino Mega Maestro, Arduino esclavos e instrumentación asociada durante la ejecución de un ensayo automatizado.

El sistema ejecuta de manera secuencial las etapas de preparación de la cámara, acondicionamiento de las condiciones de ensayo, aplicación de carga mecánica, adquisición de variables experimentales y almacenamiento de la información obtenida.

Cada etapa depende de la correcta finalización de la etapa anterior, garantizando que el ensayo se realice bajo condiciones controladas y seguras, manteniendo la sincronización entre los diferentes módulos de adquisición y control.

El Dashboard Python supervisa permanentemente el estado del sistema, registra todas las variables relevantes del proceso y proporciona al operador la información necesaria para el seguimiento del ensayo en tiempo real.

## Flujo de operación

1. El operador inicia el Dashboard H2GREEN y configura los parámetros generales del ensayo, incluyendo presión, temperatura, velocidad y tiempo de exposición.

2. El Dashboard establece la comunicación con el Arduino Mega Maestro, el cual verifica la disponibilidad de los cuatro Arduino esclavos y de los módulos de adquisición.

3. Una vez validada la comunicación, el sistema queda en estado de espera para iniciar la secuencia automática.

4. Al presionar el botón **AUTO**, el Dashboard envía la orden de inicio al Arduino Mega Maestro.

5. El sistema ejecuta automáticamente la secuencia de purga, eliminando el aire residual de la cámara de ensayo.

6. Finalizada la purga, comienza la etapa de presurización, controlando continuamente la presión mediante el Arduino esclavo de presión y las electroválvulas del sistema.

7. Al alcanzar la presión objetivo, el sistema entra en la etapa de estabilización, verificando que las condiciones de presión permanezcan dentro del rango establecido.

8. Posteriormente se inicia la etapa de exposición, manteniendo la probeta bajo las condiciones programadas durante el tiempo definido por el operador.

9. Finalizada la exposición, el Dashboard habilita el inicio del ensayo mecánico y el Arduino Mega coordina el movimiento del motor paso a paso mediante el Arduino esclavo de velocidad.

10. Durante el ensayo se adquieren continuamente las variables de fuerza, desplazamiento, presión y temperatura, transmitiéndolas al Dashboard para su visualización y registro automático.

11. Todas las variables del proceso son almacenadas en archivos CSV y utilizadas para la generación de gráficos y el análisis posterior del comportamiento del material.

12. Al finalizar el ensayo, el sistema retorna a un estado seguro, quedando disponible para la ejecución de un nuevo ensayo o para la detención completa de la plataforma.

## Implementación relacionada

- [Dashboard H2GREEN](../../python/Dashboards/Dashboard_H2Green_v1.0.py)
- [Arduino Mega Maestro](../../arduino/maestro/Mega_H2Green_v1.0.ino)

---

# Estado del Proyecto

**Versión:** Prototipo 001

### Estado actual

- ✅ Arquitectura general validada.
- ✅ Dashboard Python operativo.
- ✅ Arduino Mega Maestro operativo.
- ✅ Arduino esclavo de presión operativo.
- ✅ Arduino esclavo de fuerza operativo.
- ✅ Arduino esclavo de temperatura operativo.
- ✅ Arduino esclavo de velocidad operativo.
- 🔄 Integración de la cámara Basler en desarrollo.
- 🔄 Integración del hardware definitivo (transmisores, electroválvulas y sistema térmico).

---

**Proyecto H2GREEN**  
Universidad Técnica Federico Santa María  
Departamento de Ingeniería Mecánica – Departamento de Electrónica
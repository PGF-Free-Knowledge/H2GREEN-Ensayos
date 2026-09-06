# Desarrollo del Software H2GREEN

## Evolución del Sistema de Automatización

Este documento describe la evolución del desarrollo del software de la plataforma **H2GREEN**, indicando las funcionalidades implementadas, el estado actual de cada módulo y la hoja de ruta para las siguientes etapas.

El desarrollo se ha realizado de forma incremental, validando cada etapa antes de avanzar a la siguiente, permitiendo disponer de una plataforma estable y escalable para la automatización de ensayos de materiales en condiciones asociadas al hidrógeno.

---

# Estado General del Desarrollo

| Etapa | Funcionalidad | Estado |
|--------|---------------|:------:|
| 1 | Dashboard Python | ✅ |
| 2 | Comunicación Serial Python ↔ Arduino Mega | ✅ |
| 3 | Máquina de Estados | ✅ |
| 4 | Secuencia Automática | ✅ |
| 5 | Temporizador de Exposición | ✅ |
| 6 | Función ABORTAR | ✅ |
| 7 | Registro Automático CSV | ✅ |
| 8 | Gráficos en Tiempo Real | ✅ |
| 9 | Integración Maestro + Arduino Esclavos | ✅ |
|10 | Detección Automática de Rotura | 🚧 |
|11 | Integración Cámara Basler | 🚧 |
|12 | Control PID de Temperatura | 🚧 |
|13 | Reportes Automáticos | 🚧 |

---

# ETAPA 1 — Dashboard Python

**Estado:** ✅ Implementado

### Objetivo

Desarrollar la interfaz principal para supervisar y controlar el ensayo desde un único punto de operación.

### Descripción funcional

El Dashboard Python constituye el centro de supervisión y control de la plataforma H2GREEN. Desde esta interfaz el operador configura los parámetros del ensayo, supervisa el estado de cada subsistema y controla la ejecución de la secuencia automática.

El Dashboard centraliza la comunicación con el Arduino Mega Maestro, permitiendo visualizar en tiempo real las variables adquiridas por los diferentes módulos de instrumentación, controlar el avance de la máquina de estados y registrar toda la información generada durante el ensayo.

Además de actuar como interfaz de usuario, el Dashboard coordina la interacción entre los distintos componentes del sistema, proporcionando una plataforma única para la operación, monitoreo y almacenamiento de los datos experimentales.

### Flujo de operación

1. El operador ejecuta el Dashboard H2GREEN desde el computador de supervisión.

2. Durante el inicio, el sistema carga la interfaz gráfica, inicializa las variables de operación y prepara los módulos internos del software.

3. El Dashboard intenta establecer la comunicación serial con el Arduino Mega Maestro, verificando la disponibilidad del puerto configurado.

4. Una vez establecida la comunicación, el Dashboard habilita las funciones de supervisión y control del sistema.

5. El Dashboard comienza la adquisición continua de las variables provenientes del Arduino Mega, actualizando los indicadores y gráficos en tiempo real.

6. El operador puede configurar los parámetros del ensayo, incluyendo presión objetivo, tiempo de exposición y velocidad de desplazamiento.

7. Durante la ejecución del ensayo, el Dashboard supervisa permanentemente el estado de la máquina de estados, coordina la secuencia automática y registra todas las variables del proceso.

8. Finalizado el ensayo, el Dashboard almacena los datos experimentales, mantiene disponible el historial de registros y deja el sistema preparado para la ejecución de un nuevo ensayo.

### Funcionalidades implementadas

- Configuración del ensayo.
- Visualización de variables.
- Panel de operación.
- Gestión de estados.
- Comunicación con Arduino Mega.

---

# ETAPA 2 — Comunicación Serial

**Estado:** ✅ Implementado

### Objetivo

Establecer una comunicación bidireccional entre Python y el Arduino Mega.

### Descripción funcional

La comunicación serial constituye el enlace principal entre el Dashboard Python y el Arduino Mega Maestro, permitiendo el intercambio continuo de comandos, estados y variables de proceso durante la ejecución del ensayo.

El Dashboard actúa como sistema supervisor, enviando órdenes relacionadas con la configuración del ensayo, el inicio de la secuencia automática y las acciones del operador. El Arduino Mega interpreta estos comandos, coordina el funcionamiento de los módulos esclavos y responde con la información adquirida desde la instrumentación.

Esta comunicación bidireccional permite mantener sincronizados el software de supervisión y el sistema de control distribuido, garantizando una operación segura y una actualización continua del estado del ensayo.

### Flujo de operación

1. El Dashboard Python identifica el puerto de comunicación configurado para el Arduino Mega Maestro.

2. Al iniciar el sistema, Python establece la conexión serial y verifica que el Arduino Mega se encuentre disponible.

3. Una vez establecida la comunicación, el Dashboard envía los parámetros generales de configuración necesarios para la operación del sistema.

4. El Arduino Mega recibe los comandos provenientes del Dashboard, los interpreta y coordina la ejecución de las acciones correspondientes.

5. El Arduino Mega consulta periódicamente a los Arduino esclavos de presión, fuerza, temperatura y velocidad, recopilando la información de cada uno de ellos.

6. Las variables adquiridas son transmitidas desde el Arduino Mega hacia el Dashboard Python mediante comunicación serial.

7. El Dashboard procesa la información recibida, actualiza los indicadores, gráficos y estados del sistema, y registra las variables del ensayo.

8. Durante toda la operación, la comunicación permanece activa, permitiendo el intercambio continuo de comandos, estados y datos entre el software de supervisión y el sistema de control distribuido.

### Funcionalidades implementadas

- Envío de comandos.
- Recepción de datos.
- Protocolo serial estructurado.
- Sincronización de estados.

---

# ETAPA 3 — Máquina de Estados

**Estado:** ✅ Implementado

### Objetivo

Controlar el comportamiento del sistema mediante estados definidos.

### Descripción funcional

La máquina de estados constituye el núcleo lógico del software H2GREEN, permitiendo controlar de forma ordenada y segura cada una de las etapas del ensayo automatizado.

Cada estado representa una condición específica de operación del sistema y define las acciones que deben ejecutarse antes de permitir la transición hacia la siguiente etapa del proceso.

El Dashboard Python supervisa continuamente el estado actual del sistema, mientras que el Arduino Mega Maestro ejecuta las acciones asociadas a cada transición, coordinando el funcionamiento de los distintos módulos de control.

Esta arquitectura permite garantizar que cada etapa del ensayo se complete correctamente antes de avanzar a la siguiente, aumentando la seguridad, la trazabilidad y la repetibilidad del proceso experimental.

### Flujo de operación

1. Al iniciar el Dashboard, el sistema establece el estado inicial **DETENIDO**, manteniendo todos los módulos en condición segura.

2. El operador configura los parámetros del ensayo y verifica que la comunicación con el Arduino Mega Maestro y los módulos esclavos sea correcta.

3. Al presionar el botón **AUTO**, el Dashboard ordena al Arduino Mega iniciar la máquina de estados automática.

4. El sistema cambia al estado **PURGA**, ejecutando las acciones necesarias para acondicionar la cámara de ensayo.

5. Finalizada la purga, el sistema transita automáticamente al estado **PRESURIZANDO**, controlando el incremento de presión hasta alcanzar el valor programado.

6. Alcanzada la presión objetivo, el sistema cambia al estado **ESTABLE**, verificando que las condiciones permanezcan dentro de los límites establecidos.

7. Cumplidas las condiciones de estabilidad, el sistema pasa al estado **EXPOSICIÓN**, manteniendo la probeta bajo presión durante el tiempo configurado.

8. Finalizada la exposición, el Dashboard habilita el estado **LISTO ENSAYO**, indicando que las condiciones necesarias para iniciar el ensayo mecánico han sido alcanzadas.

9. Al iniciar el ensayo, el sistema cambia al estado **ENSAYO**, coordinando simultáneamente el movimiento del motor, la adquisición de fuerza, presión, temperatura y el registro continuo de datos.

10. Si el operador selecciona la función **ABORTAR** o se detecta una condición de seguridad, el sistema cambia inmediatamente al estado **ABORTADO**, ejecutando las acciones necesarias para detener el ensayo y dejar la plataforma en una condición segura.

### Estados implementados

- DETENIDO
- PURGA
- PRESURIZANDO
- ESTABLE
- EXPOSICIÓN
- LISTO ENSAYO
- ENSAYO
- ABORTADO

---

# ETAPA 4 — Secuencia Automática

**Estado:** ✅ Implementado

### Objetivo

Automatizar la preparación del ensayo.

### Descripción funcional

La secuencia automática permite ejecutar de forma ordenada todas las etapas necesarias para preparar la cámara de ensayo antes del inicio del ensayo mecánico, reduciendo la intervención del operador y asegurando la repetibilidad del proceso.

Una vez iniciada la secuencia, el Dashboard Python coordina el avance de la máquina de estados mientras el Arduino Mega Maestro controla la ejecución de cada etapa mediante los módulos de presión, temperatura y velocidad.

Cada transición entre estados se realiza únicamente cuando se cumplen las condiciones previamente definidas, garantizando que el ensayo comience bajo condiciones controladas de presión, temperatura y seguridad.

### Flujo de operación

1. El operador configura desde el Dashboard los parámetros generales del ensayo, incluyendo presión objetivo, tiempo de exposición y velocidad de desplazamiento.

2. Una vez verificada la configuración, el operador presiona el botón **AUTO**, iniciando la secuencia automática del sistema.

3. El Dashboard envía la orden de inicio al Arduino Mega Maestro, el cual cambia el estado del sistema a **PURGA**.

4. Durante la etapa de purga, el Arduino esclavo de presión controla las electroválvulas para acondicionar la cámara de ensayo y eliminar el aire residual.

5. Finalizada la purga, el sistema cambia automáticamente al estado **PRESURIZACIÓN**, incrementando la presión hasta alcanzar el valor programado por el operador.

6. Al alcanzar la presión objetivo, el sistema entra en la etapa de **ESTABILIZACIÓN**, verificando que las condiciones permanezcan dentro de los límites establecidos antes de continuar.

7. Una vez estabilizada la presión, comienza la etapa de **EXPOSICIÓN**, manteniendo la probeta sometida a las condiciones definidas durante el tiempo programado.

8. Finalizado el tiempo de exposición, el Dashboard cambia el estado del sistema a **LISTO ENSAYO**, habilitando el inicio del ensayo mecánico y dejando preparada la plataforma para la adquisición de datos experimentales.

### Secuencia implementada

1. Purga.
2. Presurización.
3. Estabilización.
4. Exposición.
5. Listo para ensayo.

---

# ETAPA 5 — Temporizador de Exposición

**Estado:** ✅ Implementado

### Objetivo

Controlar automáticamente el tiempo de exposición antes del ensayo.

### Descripción funcional

El temporizador de exposición controla automáticamente el tiempo durante el cual la probeta permanece sometida a las condiciones de presión establecidas antes del inicio del ensayo mecánico.

Una vez alcanzadas las condiciones de presión y estabilidad definidas por el operador, el Dashboard Python inicia una cuenta regresiva sincronizada con la máquina de estados del sistema.

Durante este período, el sistema mantiene la supervisión continua de las variables del ensayo, verificando que las condiciones permanezcan dentro de los límites establecidos antes de habilitar el inicio del ensayo mecánico.

La finalización del temporizador constituye el criterio que permite al sistema cambiar automáticamente al estado **LISTO ENSAYO**, garantizando que todas las condiciones de exposición hayan sido cumplidas.

### Flujo de operación

1. Una vez finalizada la etapa de estabilización, el Dashboard Python inicia automáticamente el temporizador de exposición utilizando el tiempo configurado por el operador.

2. El tiempo restante es actualizado continuamente en la interfaz gráfica, permitiendo al operador supervisar el avance de la exposición.

3. Durante toda la cuenta regresiva, el Arduino Mega Maestro mantiene la supervisión de los módulos de presión y temperatura, verificando que las condiciones del ensayo permanezcan dentro de los parámetros establecidos.

4. El Dashboard continúa registrando las variables del proceso y actualizando los gráficos en tiempo real, sin interrumpir la adquisición de datos.

5. Si durante la exposición se produce una condición de seguridad o el operador selecciona la función **ABORTAR**, el temporizador se detiene inmediatamente y el sistema ejecuta la secuencia de parada segura.

6. Al llegar el temporizador a cero, el Dashboard finaliza automáticamente la etapa de exposición y cambia la máquina de estados a **LISTO ENSAYO**.

7. En este estado, el sistema informa al operador que las condiciones requeridas para iniciar el ensayo mecánico han sido cumplidas y habilita las funciones correspondientes para continuar con la secuencia del proceso.

### Funcionalidades implementadas

- Temporizador configurable.
- Cuenta regresiva.
- Cambio automático de estado.
- Habilitación del ensayo.

---

# ETAPA 6 — Función ABORTAR

**Estado:** ✅ Implementado

### Objetivo

Garantizar una detención segura del sistema.

### Descripción funcional

La función **ABORTAR** constituye el mecanismo principal de seguridad del software H2GREEN, permitiendo detener inmediatamente la ejecución del ensayo cuando el operador lo solicite o cuando se detecte una condición que comprometa la seguridad del sistema.

Al activarse esta función, el Dashboard Python envía una orden inmediata al Arduino Mega Maestro para interrumpir la secuencia automática y ejecutar una detención controlada de todos los módulos involucrados en el ensayo.

Durante este proceso, el sistema detiene el movimiento del motor, finaliza las acciones de control en curso, mantiene el registro de las variables adquiridas y deja la plataforma en una condición segura antes de permitir una nueva operación.

La implementación de esta función busca proteger tanto la integridad del equipo como la seguridad del operador y de la probeta sometida a ensayo.

### Flujo de operación

1. Durante cualquier etapa del ensayo, el operador puede presionar el botón **ABORTAR** desde el Dashboard H2GREEN para solicitar la detención inmediata del sistema.

2. El Dashboard envía el comando de aborto al Arduino Mega Maestro mediante la comunicación serial establecida.

3. El Arduino Mega interrumpe la secuencia automática y notifica a los módulos esclavos que deben finalizar sus operaciones de forma controlada.

4. El sistema ordena la detención inmediata del motor paso a paso, evitando la aplicación de carga adicional sobre la probeta.

5. El módulo de presión ejecuta la secuencia de seguridad correspondiente, cerrando la alimentación de presión y habilitando la descarga controlada de la cámara cuando corresponde.

6. El Dashboard continúa registrando las variables disponibles hasta confirmar que todos los módulos han alcanzado una condición segura.

7. La máquina de estados cambia al estado **ABORTADO**, actualizando la interfaz gráfica e informando al operador que la secuencia fue interrumpida.

8. Una vez finalizada la detención segura, el sistema permanece en espera hasta que el operador reinicie el proceso o configure un nuevo ensayo.

### Funcionalidades implementadas

- Detención del motor.
- Cierre de presión.
- Apertura de purga.
- Cancelación de la secuencia automática.
- Retorno seguro al estado detenido.

---

# ETAPA 7 — Registro Automático CSV

**Estado:** ✅ Implementado

### Objetivo

Registrar automáticamente todos los datos del ensayo.

### Descripción funcional

El sistema de registro automático constituye uno de los componentes fundamentales del software H2GREEN, permitiendo almacenar de forma continua todas las variables adquiridas durante la ejecución del ensayo.

El Dashboard Python registra automáticamente la información recibida desde el Arduino Mega Maestro, generando archivos en formato CSV que contienen el historial completo de las mediciones realizadas durante cada ensayo.

Este mecanismo permite conservar la trazabilidad de los datos experimentales, facilitando su posterior procesamiento, análisis estadístico y generación de curvas de comportamiento mecánico.

El registro automático elimina la necesidad de intervención manual durante la adquisición de datos, asegurando la integridad de la información y la sincronización temporal entre todas las variables registradas.

### Flujo de operación

1. Al iniciar un nuevo ensayo, el Dashboard Python crea automáticamente un archivo CSV destinado al almacenamiento de las variables experimentales.

2. Durante la ejecución del ensayo, el Arduino Mega Maestro transmite continuamente las variables adquiridas desde los distintos módulos del sistema.

3. El Dashboard recibe la información, verifica la integridad de los datos y organiza cada medición de acuerdo con la estructura definida para el archivo de registro.

4. Cada conjunto de datos es almacenado automáticamente en una nueva fila del archivo CSV, conservando el orden cronológico de adquisición.

5. El proceso de registro se ejecuta de forma simultánea con la actualización de la interfaz gráfica y de los gráficos en tiempo real, sin afectar la operación del sistema.

6. Al finalizar el ensayo o al ejecutarse una detención segura, el Dashboard cierra correctamente el archivo CSV, garantizando la integridad de la información registrada.

7. Los archivos generados quedan disponibles para su posterior análisis, procesamiento de resultados y generación de reportes técnicos.

### Variables registradas

- Tiempo.
- Fuerza.
- Desplazamiento.
- Presión cámara.
- Presión suministro.
- Temperatura.

---

# ETAPA 8 — Gráficos en Tiempo Real

**Estado:** ✅ Implementado

### Objetivo

Visualizar el comportamiento del ensayo durante su ejecución.

### Descripción funcional

El módulo de gráficos en tiempo real permite visualizar de forma continua la evolución de las principales variables del ensayo, proporcionando al operador una representación inmediata del comportamiento del sistema.

El Dashboard Python procesa las mediciones recibidas desde el Arduino Mega Maestro y actualiza dinámicamente las gráficas durante toda la ejecución del ensayo, facilitando la supervisión de las condiciones experimentales.

La visualización en tiempo real permite detectar oportunamente variaciones en las variables medidas, verificar el correcto funcionamiento de la plataforma y apoyar la toma de decisiones durante el desarrollo del ensayo.

Además de constituir una herramienta de supervisión, los gráficos representan una primera aproximación al análisis experimental, permitiendo observar la evolución del comportamiento mecánico de la probeta mientras el ensayo se encuentra en ejecución.

### Flujo de operación

1. Una vez establecida la comunicación con el Arduino Mega Maestro, el Dashboard comienza a recibir continuamente las variables adquiridas por los diferentes módulos del sistema.

2. Cada conjunto de datos recibido es procesado por el Dashboard y utilizado para actualizar los gráficos correspondientes sin interrumpir la ejecución del ensayo.

3. La información de fuerza, desplazamiento, presión y temperatura es representada gráficamente en tiempo real, permitiendo observar la evolución de las variables durante todo el proceso experimental.

4. Los gráficos son actualizados de forma continua mientras el sistema permanece en estado de ensayo, proporcionando una visualización inmediata del comportamiento de la probeta y de las condiciones de operación.

5. Paralelamente a la actualización gráfica, el Dashboard continúa registrando todas las variables en el archivo CSV, manteniendo sincronizados el registro de datos y la representación visual.

6. El operador puede utilizar los gráficos para verificar el correcto funcionamiento del sistema, detectar comportamientos anómalos y supervisar la evolución del ensayo sin detener la adquisición de datos.

7. Al finalizar el ensayo, los gráficos muestran el comportamiento completo registrado durante la prueba, constituyendo una referencia inmediata para el análisis preliminar de los resultados obtenidos.

### Gráficos implementados

- Fuerza vs Tiempo.
- Desplazamiento vs Tiempo.
- Fuerza vs Desplazamiento.

---

# ETAPA 9 — Integración Maestro + Arduino Esclavos

**Estado:** ✅ Implementado

### Objetivo

Coordinar el funcionamiento del sistema distribuido.

### Descripción funcional

La arquitectura distribuida implementada en H2GREEN utiliza un Arduino Mega como controlador maestro y cuatro Arduino Uno dedicados a funciones específicas de adquisición y control.

Esta distribución de tareas permite desacoplar las diferentes funciones del sistema, facilitando el mantenimiento, la escalabilidad del proyecto y la incorporación de nuevos módulos sin afectar el funcionamiento general de la plataforma.

El Arduino Mega Maestro actúa como coordinador principal, administrando la comunicación con cada Arduino esclavo, consolidando la información recibida y ejecutando las órdenes provenientes del Dashboard Python.

Cada Arduino esclavo opera de manera independiente sobre su respectivo subsistema, mientras que el Arduino Mega sincroniza la operación global, asegurando que todos los módulos trabajen de forma coordinada durante el ensayo.

### Flujo de operación

1. Al iniciar el Dashboard H2GREEN, el Arduino Mega Maestro establece la comunicación con cada uno de los Arduino esclavos que conforman la arquitectura distribuida del sistema.

2. Cada Arduino esclavo inicializa el hardware asociado a su función específica, verificando el correcto funcionamiento de los dispositivos bajo su responsabilidad.

3. El Arduino Mega consulta periódicamente a cada módulo esclavo, recopilando las variables de presión, fuerza, temperatura y estado del sistema.

4. La información recibida desde los módulos esclavos es consolidada por el Arduino Mega y transmitida al Dashboard Python mediante comunicación serial.

5. El Dashboard procesa la información recibida, actualiza los indicadores de la interfaz gráfica, registra las variables del ensayo y mantiene sincronizada la máquina de estados.

6. Cuando el operador ejecuta una acción desde el Dashboard, el Arduino Mega interpreta el comando recibido y lo distribuye únicamente al Arduino esclavo responsable de ejecutar dicha función.

7. Durante toda la ejecución del ensayo, el Arduino Mega coordina el intercambio permanente de información entre los módulos esclavos y el Dashboard, garantizando la sincronización del sistema distribuido.

8. Esta arquitectura modular facilita la incorporación de nuevos dispositivos de adquisición y control, permitiendo ampliar las capacidades de la plataforma sin modificar la estructura general del software.

### Módulos integrados

- Arduino Mega Maestro.
- Arduino Presión.
- Arduino Fuerza.
- Arduino Temperatura.
- Arduino Velocidad.

---

# ETAPA 10 — Detección Automática de Rotura

**Estado:** 🚧 En desarrollo

### Objetivo

Detectar automáticamente la rotura de la probeta mediante el análisis de la fuerza y finalizar el ensayo de forma segura.

---

# ETAPA 11 — Integración Cámara Basler

**Estado:** 🚧 En desarrollo

### Objetivo

Incorporar la medición real de desplazamiento mediante visión artificial utilizando la cámara Basler y el software Pylon.

---

# ETAPA 12 — Control PID de Temperatura

**Estado:** 🚧 En desarrollo

### Objetivo

Implementar un control térmico en lazo cerrado utilizando un controlador PID, un SSR y el calefactor de la cámara.

---

# ETAPA 13 — Reportes Automáticos

**Estado:** 🚧 En desarrollo

### Objetivo

Generar automáticamente un informe completo del ensayo con resultados, gráficos y parámetros registrados.

---

# Próximas Etapas

El desarrollo continuará siguiendo el siguiente orden:

1. Detección automática de rotura.
2. Integración de la cámara Basler.
3. Control PID de temperatura.
4. Reportes automáticos de ensayo.

---

# Resumen

Actualmente la plataforma dispone de una arquitectura funcional completamente operativa para la ejecución de ensayos automatizados, encontrándose en una etapa de transición hacia la integración del hardware industrial definitivo y la incorporación de funciones avanzadas de inteligencia y automatización.

---

**Proyecto H2GREEN**

Universidad Técnica Federico Santa María

Departamento de Ingeniería Mecánica – Departamento de Electrónica
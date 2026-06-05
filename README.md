# H2GREEN - Plataforma Automatizada de Ensayo para Evaluación de Materiales en Condiciones Asociadas a Hidrógeno

## Descripción General

Este proyecto corresponde al desarrollo de una plataforma automatizada de ensayo orientada a la evaluación de materiales sometidos a condiciones controladas de presión, temperatura y carga mecánica, con aplicación en estudios relacionados con fragilización por hidrógeno y validación de materiales para sistemas de hidrógeno.

La plataforma está siendo desarrollada como apoyo a la iniciativa **H2 Green**, permitiendo la generación de datos experimentales locales mediante una arquitectura distribuida basada en Python y Arduino.

---

# Objetivos del Sistema

* Automatizar la secuencia completa de ensayo.
* Controlar presión, temperatura y velocidad de ensayo.
* Medir fuerza y desplazamiento de probetas.
* Registrar datos experimentales en tiempo real.
* Generar curvas esfuerzo-deformación.
* Integrar visión artificial mediante cámara Basler.
* Incorporar funciones de seguridad y monitoreo continuo.

---

# Arquitectura General

## Nivel de Supervisión

### Dashboard Python

Funciones principales:

* Supervisión del proceso.
* Registro CSV.
* Visualización en tiempo real.
* Gestión de estados.
* Control de secuencia automática.
* Alarmas y eventos.
* Integración futura con cámara Basler.

---

## Nivel de Control

### Arduino Mega 2560 (Maestro)

Responsabilidades:

* Coordinación de esclavos.
* Comunicación serial con Python.
* Sincronización de eventos.
* Consolidación de datos.
* Distribución de comandos.

---

## Nivel de Adquisición y Control Distribuido

### Arduino Uno – Esclavo Presión

Funciones:

* Lectura de PT-01.
* Lectura de PT-02.
* Control de válvula HVL1.
* Control de válvula HVL2.
* Secuencia de purga.
* Presurización automática.

---

### Arduino Uno – Esclavo Fuerza

Funciones:

* Lectura de celda de carga 20 kN.
* Acondicionamiento mediante HX711.
* Envío de datos al maestro.

---

### Arduino Uno – Esclavo Temperatura

Funciones:

* Lectura de sensor de temperatura.
* Control futuro mediante PID.
* Activación de SSR.
* Regulación térmica de la cámara de ensayo.

---

### Arduino Uno – Esclavo Velocidad

Funciones:

* Control del driver SH-1108.
* Control del motor paso a paso.
* Gestión de velocidad de ensayo.
* Seguimiento de posición.

---

# Instrumentación Principal

## Presión

* PT-01: Presión cámara de ensayo.
* PT-02: Presión suministro.
* Transmisores industriales 4–20 mA (pendiente integración física).

---

## Fuerza

* Celda de carga 20 kN.
* HX711.

---

## Temperatura

* Sensor DS18B20.
* SSR.
* Calefactor de cartucho.

---

## Desplazamiento

* Cámara Basler.
* Software Pylon.
* Procesamiento directo en Python.

---

# Secuencia Operacional

El sistema implementa la siguiente máquina de estados:

```text
INICIO
   ↓
PURGA
   ↓
PRESURIZACIÓN
   ↓
ESTABILIZACIÓN
   ↓
EXPOSICIÓN
   ↓
LISTO ENSAYO
   ↓
ENSAYO
   ↓
FINALIZACIÓN
```

---

# Seguridad

El sistema incorpora:

* Función ABORTAR.
* Detención segura del motor.
* Apertura automática de purga.
* Cierre de presión.
* Bloqueo de ensayo antes de exposición.
* Gestión de estados seguros.

---

# Estado Actual del Proyecto

## Implementado

* Dashboard Python.
* Comunicación serial.
* Arduino Mega maestro.
* Esclavo presión.
* Esclavo fuerza.
* Esclavo temperatura.
* Esclavo velocidad.
* Registro CSV.
* Gráficos en tiempo real.
* Secuencia automática.
* Temporizador de exposición.
* Función ABORTAR.
* Control de versiones mediante Git y GitHub.

---

## En Desarrollo

* Detección automática de rotura.
* Control PID de temperatura.
* Integración de cámara Basler.
* Generación automática de reportes.
* Integración de hardware industrial definitivo.

---

# Hardware Pendiente de Integración

* Transmisores IFM 4–20 mA.
* Válvulas HVL1 y HVL2.
* SSR industrial.
* Calefactor de cámara.
* Cámara Basler.
* Accesorios de presión y seguridad.

---

# Tecnologías Utilizadas

## Software

* Python 3.12
* PyQt5
* PyQtGraph
* Visual Studio Code
* Git
* GitHub

## Hardware

* Arduino Mega 2560
* Arduino Uno
* HX711
* DS18B20
* Driver SH-1108
* Motor Stepper 86HS156-6204A14-B35-04

---

# Repositorio

Proyecto en desarrollo asociado a la iniciativa H2 Green para evaluación de materiales en condiciones asociadas a hidrógeno.

Versión Base Oficial:

H2GREEN v1.0

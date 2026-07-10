# Diagramas del Proyecto H2GREEN

Esta carpeta contiene los diagramas oficiales del proyecto **H2GREEN**, desarrollados para documentar la arquitectura del sistema, los lazos de control y la secuencia operacional del prototipo de ensayo automatizado para evaluación de materiales en condiciones asociadas al hidrógeno.

---

# 01. Arquitectura General del Sistema

**Archivo:** `01_Arquitectura_General_del_Sistema.png`

Presenta la arquitectura completa del sistema, mostrando la interacción entre el Dashboard desarrollado en Python, el Arduino Mega Maestro, los cuatro Arduino esclavos, la cámara Basler y los dispositivos de campo.

### Implementación relacionada

- [Dashboard H2GREEN](../../python/Dashboards/Dashboard_H2Green_v1.0.py)
- [Arduino Mega Maestro](../../arduino/maestro/Mega_H2Green_v1.0.ino)
- [Arduino Presión](../../arduino/presion/Presion_H2Green_v1.0.ino)
- [Arduino Fuerza](../../arduino/fuerza/Fuerza_H2Green_v1.0.ino)
- [Arduino Temperatura](../../arduino/temperatura/Temperatura_H2Green_v1.0.ino)
- [Arduino Velocidad](../../arduino/velocidad/Velocidad_H2Green_v1.0.ino)

---

# 02. Secuencia Detallada del Lazo de Presión

**Archivo:** `02_Secuencia_Detallada_Lazo_de_Presion.png`

Describe el funcionamiento del lazo de presión, incluyendo purga, presurización, estabilización, monitoreo y control de las electroválvulas.

### Código asociado

- [Arduino Presión](../../arduino/presion/Presion_H2Green_v1.0.ino)
- [Dashboard H2GREEN](../../python/Dashboards/Dashboard_H2Green_v1.0.py)

---

# 03. Secuencia Detallada del Lazo de Temperatura

**Archivo:** `03_Secuencia_Detallada_Lazo_de_Temperatura.png`

Describe el sistema de control de temperatura mediante el Arduino esclavo, el sensor DS18B20, el relé de estado sólido (SSR) y el calefactor.

### Código asociado

- [Arduino Temperatura](../../arduino/temperatura/Temperatura_H2Green_v1.0.ino)
- [Dashboard H2GREEN](../../python/Dashboards/Dashboard_H2Green_v1.0.py)

---

# 04. Secuencia Detallada del Lazo de Desplazamiento del Motor

**Archivo:** `04_Secuencia_Detallada_Lazo_de_Desplazamiento_Motor.png`

Presenta el control del motor paso a paso mediante el driver SH-1108 y el Arduino esclavo de velocidad.

### Código asociado

- [Arduino Velocidad](../../arduino/velocidad/Velocidad_H2Green_v1.0.ino)
- [Dashboard H2GREEN](../../python/Dashboards/Dashboard_H2Green_v1.0.py)

---

# 05. Secuencia Detallada del Lazo de Fuerza y Desplazamiento

**Archivo:** `05_Secuencia_Detallada_Lazo_de_Fuerza_y_Desplazamiento.png`

Describe la adquisición de fuerza mediante la celda de carga KIS y el módulo HX711, junto con el desplazamiento obtenido mediante la cámara Basler para generar las curvas Fuerza–Desplazamiento y Esfuerzo–Deformación.

### Código asociado

- [Arduino Fuerza](../../arduino/fuerza/Fuerza_H2Green_v1.0.ino)
- [Dashboard H2GREEN](../../python/Dashboards/Dashboard_H2Green_v1.0.py)

---

# 06. Secuencia Completa del Proceso

**Archivo:** `06_Secuencia_Completa_del_Proceso.png`

Resume la operación completa del sistema, integrando todos los lazos de control desde el inicio del ensayo hasta la generación de resultados.

### Código asociado

- [Dashboard H2GREEN](../../python/Dashboards/Dashboard_H2Green_v1.0.py)
- [Arduino Mega Maestro](../../arduino/maestro/Mega_H2Green_v1.0.ino)

---

# Estado del proyecto

**Versión del sistema:** Prototipo 001

**Estado actual:**

- ✔ Arquitectura general validada.
- ✔ Dashboard Python operativo.
- ✔ Arduino Mega Maestro operativo.
- ✔ Cuatro Arduino esclavos operativos.
- ✔ Integración de la cámara Basler en desarrollo.
- ✔ Integración progresiva de hardware definitivo (transmisores de presión, electroválvulas y sistema térmico).

---

## Estructura del proyecto relacionada

```text
arduino/
├── maestro/
├── presion/
├── fuerza/
├── temperatura/
└── velocidad/

python/
└── Dashboards/
```

---

**Proyecto H2GREEN**

**Universidad Técnica Federico Santa María**  
Departamento de Ingeniería Mecánica / Departamento de Electrónica
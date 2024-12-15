# ModFusionAI

### **Descripción**
ModFusionAI es un proyecto diseñado para fusionar archivos de mods en el juego Red Dead Redemption 2, asegurando la compatibilidad entre diferentes paquetes (por ejemplo, Whyem's DLC y Red Dead Offline).

El proyecto utiliza técnicas de aprendizaje automático para mantener la estructura jerárquica de los archivos `.ymt`, prediciendo dónde deberían estar los elementos fusionados. También genera reportes detallados para depurar posibles errores.

---

### **Características principales**
- Predicción automática de estructuras utilizando Random Forest.
- Generación de reportes para validar la fusión.
- Optimización continua del flujo de trabajo.

---

### **Requisitos**
- **Python 3.8 o superior**
- **Librerías necesarias**:
  ```bash
  pip install pandas scikit-learn tqdm

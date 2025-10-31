## archivo con las herramientas del agente nutricional

def calcular_tmb(peso, altura, edad, genero):
    genero_normalizado = genero.lower()
    tmb = 0
    if genero_normalizado == "hombre":
        tmb = 10 * peso + 6.25 * altura - 5 * edad + 5
    elif genero_normalizado == "mujer":
        tmb = 10 * peso + 6.25 * altura - 5 * edad - 161
    else:
        raise ValueError("Género no reconocido. Debe ser 'hombre' o 'mujer'.")
        pass

    return tmb

def calcular_tdee(tmb, nivel_actividad):

    nivel_actividad = nivel_actividad.lower()
    if nivel_actividad == "sedentario":
        tdee = tmb * 1.2
    elif nivel_actividad == "ligero":
        tdee = tmb * 1.375  
    elif nivel_actividad == "moderado":
        tdee = tmb * 1.55
    elif nivel_actividad == "intenso":
        tdee = tmb * 1.725
    elif nivel_actividad == "muy intenso":
        tdee = tmb * 1.9
    else:
        raise ValueError("Nivel de actividad no reconocido.")
        pass
    return

def calcular_macros(tdee, objetivo):
    objetivo = objetivo.lower()
    
    if objetivo == "perder peso":
        prot_perc, carb_perc, fat_perc = 0.3, 0.45, 0.25
        calorias_objetivo = tdee - 500
    elif objetivo == "mantener peso":
        prot_perc, carb_perc, fat_perc = 0.25, 0.50, 0.25
        calorias_objetivo = tdee
    elif objetivo == "ganar peso":
        prot_perc, carb_perc, fat_perc = 0.30, 0.40, 0.30
        calorias_objetivo = tdee + 500
    else:
        raise ValueError("Objetivo no reconocido.")
        pass

    proteinas = (prot_perc * calorias_objetivo) / 4  
    grasas = ( fat_perc* calorias_objetivo) / 9     
    carbohidratos = ( carb_perc * calorias_objetivo) / 4  

    return {
        "calorias": calorias_objetivo,
        "proteinas_g": proteinas,
        "grasas_g": grasas,
        "carbohidratos_g": carbohidratos
    }
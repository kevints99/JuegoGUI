import tkinter as tk
from tkinter import messagebox

# Lógica del juego (igual que consola, adaptado para usar en GUI)
class Personaje:
    def __init__(self, vida, ataque, defensa):
        self.__vida = max(0, min(100, vida))
        self.__ataque = ataque
        self.__defensa = defensa

    def get_vida(self):
        return self.__vida

    def set_vida(self, nueva_vida):
        self.__vida = max(0, min(100, nueva_vida))

    def get_ataque(self):
        return self.__ataque

    def get_defensa(self):
        return self.__defensa

    def esta_vivo(self):
        return self.__vida > 0

    def atacar(self, objetivo):
        raise NotImplementedError("Implementar en subclases.")


class Guerrero(Personaje):
    def atacar(self, objetivo):
        daño = max(0, self.get_ataque() * 1.2 - objetivo.get_defensa())
        objetivo.set_vida(objetivo.get_vida() - daño)
        return f"⚔️ Guerrero ataca e inflige {daño:.1f} de daño."


class Mago(Personaje):
    def atacar(self, objetivo):
        daño = self.get_ataque()
        objetivo.set_vida(objetivo.get_vida() - daño)
        return f"✨ Mago lanza hechizo e inflige {daño:.1f} de daño (ignora defensa)."


class Arquero(Personaje):
    def atacar(self, objetivo):
        if self.get_ataque() > objetivo.get_defensa():
            daño = (self.get_ataque() - objetivo.get_defensa()) * 2
            tipo = "crítico"
        else:
            daño = max(0, self.get_ataque() - objetivo.get_defensa())
            tipo = "normal"
        objetivo.set_vida(objetivo.get_vida() - daño)
        return f"🏹 Arquero ataca ({tipo}) e inflige {daño:.1f} de daño."


# Interfaz gráfica
class JuegoGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Guardians of the Ancient Kingdom")

        self.jugador1 = None
        self.jugador2 = None
        self.turno = 0

        self.label_info = tk.Label(root, text="Selecciona personaje para Jugador 1", font=("Arial", 12))
        self.label_info.pack(pady=10)

        self.botones_frame = tk.Frame(root)
        self.botones_frame.pack()

        for personaje in ["Guerrero", "Mago", "Arquero"]:
            btn = tk.Button(self.botones_frame, text=personaje, width=10,
                            command=lambda p=personaje: self.seleccionar_personaje(p))
            btn.pack(side=tk.LEFT, padx=10)

        self.text_area = tk.Text(root, height=10, width=50, state="disabled", font=("Courier", 10))
        self.text_area.pack(pady=10)

        self.boton_ataque = tk.Button(root, text="Atacar", state="disabled", command=self.realizar_turno)
        self.boton_ataque.pack()

    def seleccionar_personaje(self, tipo):
        personaje = self.crear_personaje(tipo)
        if not self.jugador1:
            self.jugador1 = personaje
            self.label_info.config(text="Selecciona personaje para Jugador 2")
        elif not self.jugador2:
            self.jugador2 = personaje
            self.label_info.config(text="¡Batalla lista!")
            self.boton_ataque.config(state="normal")
            self.escribir(f"Jugadores listos: Jugador 1 ({type(self.jugador1).__name__}) vs Jugador 2 ({type(self.jugador2).__name__})")
        else:
            messagebox.showinfo("Juego", "Ya se han seleccionado los dos personajes.")

    def crear_personaje(self, tipo):
        if tipo == "Guerrero":
            return Guerrero(100, 30, 20)
        elif tipo == "Mago":
            return Mago(80, 40, 10)
        elif tipo == "Arquero":
            return Arquero(90, 35, 15)

    def realizar_turno(self):
        if not (self.jugador1 and self.jugador2):
            return

        if self.turno % 2 == 0:
            mensaje = self.jugador1.atacar(self.jugador2)
        else:
            mensaje = self.jugador2.atacar(self.jugador1)

        self.turno += 1
        self.escribir(f"\nTurno {self.turno}:\n{mensaje}")
        self.escribir(f"Vida Jugador 1: {self.jugador1.get_vida():.1f}")
        self.escribir(f"Vida Jugador 2: {self.jugador2.get_vida():.1f}")

        if not self.jugador1.esta_vivo() or not self.jugador2.esta_vivo():
            ganador = "Jugador 1" if self.jugador1.esta_vivo() else "Jugador 2"
            self.escribir(f"\n🎉 ¡{ganador} ha ganado!")
            self.boton_ataque.config(state="disabled")

    def escribir(self, texto):
        self.text_area.config(state="normal")
        self.text_area.insert(tk.END, texto + "\n")
        self.text_area.config(state="disabled")
        self.text_area.see(tk.END)


if __name__ == "__main__":
    root = tk.Tk()
    app = JuegoGUI(root)
    root.mainloop()

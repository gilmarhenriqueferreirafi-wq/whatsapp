import customtkinter as ctk
import pywhatkit
import threading
import time
from datetime import datetime


# ============================================================
# CONFIGURAÇÕES
# ============================================================

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


# ============================================================
# APLICATIVO
# ============================================================

class WhatsAppBot(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("WhatsApp Auto Messenger")
        self.geometry("650x700")
        self.resizable(False, False)

        # Controle da thread
        self.executando = False
        self.thread = None

        self.criar_interface()

    # ========================================================
    # INTERFACE
    # ========================================================

    def criar_interface(self):

        titulo = ctk.CTkLabel(
            self,
            text="WhatsApp Auto Messenger",
            font=ctk.CTkFont(size=28, weight="bold")
        )
        titulo.pack(pady=(25, 5))

        subtitulo = ctk.CTkLabel(
            self,
            text="Envio automático de mensagens pelo WhatsApp Web",
            text_color="gray"
        )
        subtitulo.pack(pady=(0, 20))

        # ----------------------------------------------------
        # NÚMERO
        # ----------------------------------------------------

        frame_numero = ctk.CTkFrame(self)
        frame_numero.pack(fill="x", padx=35, pady=8)

        ctk.CTkLabel(
            frame_numero,
            text="Número do WhatsApp",
            font=ctk.CTkFont(weight="bold")
        ).pack(anchor="w", padx=15, pady=(12, 3))

        self.numero_entry = ctk.CTkEntry(
            frame_numero,
            placeholder_text="+5533999999999"
        )
        self.numero_entry.pack(fill="x", padx=15, pady=(0, 12))

        # ----------------------------------------------------
        # MENSAGEM
        # ----------------------------------------------------

        frame_mensagem = ctk.CTkFrame(self)
        frame_mensagem.pack(fill="x", padx=35, pady=8)

        ctk.CTkLabel(
            frame_mensagem,
            text="Mensagem",
            font=ctk.CTkFont(weight="bold")
        ).pack(anchor="w", padx=15, pady=(12, 3))

        self.mensagem_text = ctk.CTkTextbox(
            frame_mensagem,
            height=100
        )
        self.mensagem_text.pack(fill="x", padx=15, pady=(0, 12))

        # ----------------------------------------------------
        # CONFIGURAÇÕES
        # ----------------------------------------------------

        frame_config = ctk.CTkFrame(self)
        frame_config.pack(fill="x", padx=35, pady=8)

        # Intervalo
        ctk.CTkLabel(
            frame_config,
            text="Intervalo entre mensagens (minutos)"
        ).grid(row=0, column=0, padx=15, pady=(15, 5), sticky="w")

        self.intervalo_entry = ctk.CTkEntry(
            frame_config,
            width=100
        )
        self.intervalo_entry.insert(0, "1")
        self.intervalo_entry.grid(
            row=1,
            column=0,
            padx=15,
            pady=(0, 15),
            sticky="w"
        )

        # Quantidade
        ctk.CTkLabel(
            frame_config,
            text="Quantidade de mensagens"
        ).grid(row=0, column=1, padx=15, pady=(15, 5), sticky="w")

        self.quantidade_entry = ctk.CTkEntry(
            frame_config,
            width=100
        )
        self.quantidade_entry.insert(0, "10")
        self.quantidade_entry.grid(
            row=1,
            column=1,
            padx=15,
            pady=(0, 15),
            sticky="w"
        )

        # ----------------------------------------------------
        # CONTAGEM
        # ----------------------------------------------------

        self.contagem_label = ctk.CTkLabel(
            self,
            text="Próximo envio: --:--",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        self.contagem_label.pack(pady=(15, 5))

        # ----------------------------------------------------
        # BOTÕES
        # ----------------------------------------------------

        frame_botoes = ctk.CTkFrame(self, fg_color="transparent")
        frame_botoes.pack(pady=10)

        self.iniciar_button = ctk.CTkButton(
            frame_botoes,
            text="▶  INICIAR",
            width=180,
            height=45,
            command=self.iniciar
        )
        self.iniciar_button.grid(row=0, column=0, padx=8)

        self.parar_button = ctk.CTkButton(
            frame_botoes,
            text="■  PARAR",
            width=180,
            height=45,
            fg_color="#9b2c2c",
            hover_color="#c53030",
            command=self.parar
        )
        self.parar_button.grid(row=0, column=1, padx=8)

        # ----------------------------------------------------
        # STATUS
        # ----------------------------------------------------

        ctk.CTkLabel(
            self,
            text="Status",
            font=ctk.CTkFont(weight="bold")
        ).pack(anchor="w", padx=35, pady=(10, 3))

        self.status_text = ctk.CTkTextbox(
            self,
            height=100
        )
        self.status_text.pack(
            fill="both",
            expand=True,
            padx=35,
            pady=(0, 20)
        )

        self.log("Programa iniciado.")
        self.log("Preencha os dados e clique em INICIAR.")

    # ========================================================
    # LOG
    # ========================================================

    def log(self, texto):

        horario = datetime.now().strftime("%H:%M:%S")

        self.after(
            0,
            lambda: self._adicionar_log(
                f"[{horario}] {texto}"
            )
        )

    def _adicionar_log(self, texto):

        self.status_text.insert("end", texto + "\n")
        self.status_text.see("end")

    # ========================================================
    # INICIAR
    # ========================================================

    def iniciar(self):

        if self.executando:
            return

        numero = self.numero_entry.get().strip()
        mensagem = self.mensagem_text.get("1.0", "end").strip()

        # Validação do número
        if not numero:
            self.log("ERRO: informe o número do WhatsApp.")
            return

        if not numero.startswith("+"):
            self.log("ERRO: o número deve começar com +.")
            self.log("Exemplo: +5533999999999")
            return

        # Validação da mensagem
        if not mensagem:
            self.log("ERRO: escreva uma mensagem.")
            return

        # Intervalo
        try:
            intervalo = float(
                self.intervalo_entry.get().replace(",", ".")
            )

            if intervalo <= 0:
                raise ValueError

        except ValueError:
            self.log("ERRO: intervalo inválido.")
            return

        # Quantidade
        try:
            quantidade = int(
                self.quantidade_entry.get()
            )

            if quantidade <= 0:
                raise ValueError

        except ValueError:
            self.log("ERRO: quantidade inválida.")
            return

        # Começa a execução
        self.executando = True

        self.iniciar_button.configure(
            state="disabled"
        )

        self.log("Automação iniciada.")
        self.log(f"Destino: {numero}")
        self.log(f"Quantidade: {quantidade}")
        self.log(f"Intervalo: {intervalo} minuto(s).")

        self.thread = threading.Thread(
            target=self.executar_envio,
            args=(
                numero,
                mensagem,
                intervalo,
                quantidade
            ),
            daemon=True
        )

        self.thread.start()

    # ========================================================
    # EXECUÇÃO
    # ========================================================

    def executar_envio(
        self,
        numero,
        mensagem,
        intervalo,
        quantidade
    ):

        try:

            for contador in range(1, quantidade + 1):

                if not self.executando:
                    break

                self.log(
                    f"Preparando mensagem "
                    f"{contador}/{quantidade}..."
                )

                # PyWhatKit abre o WhatsApp Web e envia
                # a mensagem.
                pywhatkit.sendwhatmsg_instantly(
                    numero,
                    mensagem,
                    wait_time=15,
                    tab_close=True,
                    close_time=3
                )

                self.log(
                    f"Mensagem {contador}/{quantidade} enviada."
                )

                # Se foi a última, termina
                if contador >= quantidade:
                    break

                # Converte minutos para segundos
                segundos = int(intervalo * 60)

                self.log(
                    f"Aguardando {intervalo} minuto(s) "
                    f"para o próximo envio..."
                )

                # Contagem regressiva
                while segundos > 0:

                    if not self.executando:
                        break

                    minutos_restantes = segundos // 60
                    segundos_restantes = segundos % 60

                    texto = (
                        f"Próximo envio: "
                        f"{minutos_restantes:02d}:"
                        f"{segundos_restantes:02d}"
                    )

                    self.after(
                        0,
                        lambda t=texto:
                        self.contagem_label.configure(text=t)
                    )

                    time.sleep(1)

                    segundos -= 1

                if not self.executando:
                    break

            if self.executando:
                self.log("Automação concluída.")
            else:
                self.log("Automação interrompida.")

        except Exception as erro:

            self.log(
                f"ERRO durante o envio: {erro}"
            )

        finally:

            self.executando = False

            self.after(
                0,
                self.finalizar_interface
            )

    # ========================================================
    # PARAR
    # ========================================================

    def parar(self):

        if not self.executando:
            self.log("Nenhuma automação está em execução.")
            return

        self.executando = False

        self.log("Solicitação para parar recebida.")

        self.contagem_label.configure(
            text="Próximo envio: --:--"
        )

    # ========================================================
    # FINALIZAR INTERFACE
    # ========================================================

    def finalizar_interface(self):

        self.iniciar_button.configure(
            state="normal"
        )

        self.contagem_label.configure(
            text="Próximo envio: --:--"
        )


# ============================================================
# INICIAR PROGRAMA
# ============================================================

if __name__ == "__main__":

    app = WhatsAppBot()

    app.mainloop()
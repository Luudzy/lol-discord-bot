# lol-discord-bot
Um bot feito para consultar dados de partidas e perfis (estilo "op.gg") diretamente pelo Discord.

---

## 🚀 Como Usar

1. Vá até o **Discord Developer Portal** e crie uma nova aplicação/bot.
2. Copie o **Token do Bot**.
3. Acesse o **Riot Developer Portal**, faça login com sua conta Riot e gere sua chave de API (**Development API Key**).
4. Copie a chave (fique atento à data de validade de 24h caso use uma chave de desenvolvedor comum).
5. Insira ambos os tokens nos seus respectivos campos no arquivo de configuração/código:

<div align="left">
  <img src="https://github.com/Luudzy/lol-discord-bot/assets/126820236/5ba26688-a2d1-48cf-b746-811dcf2f39d8" alt="Tokens Setup" width="600" />
</div>

<br clear="left" />

6. No Discord, ative o *Modo de Desenvolvedor*, clique com o botão direito no canal de texto desejado e selecione **Copiar ID do Canal**:

<div align="left">
  <img src="https://github.com/Luudzy/lol-discord-bot/assets/126820236/aaf21ad2-5aa4-46d0-869b-8451f7033f8a" alt="Discord Channel ID" width="450" />
</div>

<br clear="left" />

7. Substitua o ID copiado no campo correspondente no código:

<div align="left">
  <img src="https://github.com/Luudzy/lol-discord-bot/assets/126820236/76dbe036-7bbd-49ff-bb57-12ffb97cae89" alt="Config Channel ID" width="600" />
</div>

<br clear="left" />

8. Instale as dependências necessárias executando no terminal:

```bash
pip install discord requests

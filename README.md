# anadrop - geração automatizada de script DNS RPZ from url do pdf da Anatel

- Baixa arquivo pdf da url enviada pela Anatel
- Extrair as URLS para serem bloqueadas
- Gerar arqvuivo para DNS bind, para uso do PTZ

<section>
   <h3>Para rodar via prompt de comando:</h3>
   <pre>
  cd /anatel
  ./import_from_url.py https://sistemas.anatel.gov.br/anexar-api/publico/anexos/download/5e68ae83f4826fdb20f8f553447008f3
</pre>
</section>

<section>
   <h3>Para baixar o arquivo DNS pronto para uso:</h3>
   <pre>

http://anadrop.mycore.com.br:1984/anadrop

</pre>
</section>
- Scrip para colocar no bind [ /etc/bind/scripts/anadrop.sh ]:

<p>
<section>
   <h3>Conteúdo anadrop.sh:</h3>
   <pre>
#!/bin/sh
wget --no-check-certificate --tries=3000 --retry-connrefused --timeout=10 --dns-timeout=8 --wait=7 --waitretry=3 http://anadrop.mycore.com.br:1984/anadrop -O /etc/bind/rpz/db.rpz.zone.hosts
systemctl restart bind9
</pre>
</section>
</p>

<p>
<section>
   <h3>Crontab:</h3>
   <pre>
echo '00 00 \* \* \* root sh /etc/bind/scripts/anadrop.sh' >> /etc/crontab
</pre>
</section>
</p>

_anadrop_ &copy; 2024, Mycore Tecnologia - Released under the MIT License.

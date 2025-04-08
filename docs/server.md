[Home](/btt-ai/) |
[Add-on](/btt-ai/addon) |
[Server](/btt-ai/server) |
[Support](https://github.com/moixllik/btt-ai/issues)

---

## AI-Generative Server

```bash
make venv
make install

# Load ./venv/bin/activate
make run
```


## Text to Speech

```bash
curl -X POST http://localhost:8080?lang=en
  -H "Content-Type: application/json"
  -d '{"category":"speech","text":"Content"}'
```
         
## Text to Image

```bash
curl -X POST http://localhost:8080
  -H "Content-Type: application/json"
  -d '{"category":"image","height":1920,"width":1080,"text":"Content"}'
```

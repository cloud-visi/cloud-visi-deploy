# Contributing

This repository accepts deployment fixes and documentation improvements. Product implementation is maintained separately.

Run the local checks before proposing a change:

```bash
python3 -m pip install -r requirements-dev.txt
helm lint charts/cloud-visi
python3 -m unittest discover -s tests -v
```

Keep partner documentation clear and free of em dashes. Explain prerequisites and installation steps. Do not prescribe evaluation tasks or what partners should conclude about the product.

Never add tokens, state files, local `.env` files, backups, private product source, or partner data. Preview package publication waits for an approved licence and image evaluation terms.

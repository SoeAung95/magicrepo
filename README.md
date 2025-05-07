# GitGab Identity Dashboard

**magicrepo** is a lightweight, Web3-ready GitHub Pages site that hosts the **GitGab Identity Dashboard** — a public identity hub for decentralized profiles, badges, and contributions. Built and maintained by [SoeAung95](https://github.com/SoeAung95).

## Live Demo

> Access the live dashboard here:  
> **https://magicstone.online**

## Features

- Custom domain via Cloudflare: `magicstone.online`
- Hosted on GitHub Pages (main branch)
- Decentralized identity display from `identity.json`
- Auto-rendered Web3 tags: wallets, platforms, badges
- Fully responsive, mobile-friendly layout
- Zero JavaScript frameworks (Vanilla only)
- Open source and portable

## Files & Structure

```plaintext
magicrepo/
├── index.html           # Main page with dashboard logic
├── identity.json        # Public identity info (editable)
├── CNAME                # Domain setup for GitHub Pages
├── .gitignore           # Ignoring system/temp files
├── README.md            # This file
├── package-lock.json    # Dependency lock (optional)
└── start.sh             # Optional startup script

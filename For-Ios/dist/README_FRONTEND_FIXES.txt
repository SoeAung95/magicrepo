Fixes applied to frontend bundle (performed by assistant):
1. Renamed files with accidental double .js extension:
	 - ghost-system.js.js -> ghost-system.js
	 - ai.js.js -> ai.js
2. Updated ghost.html to remove the missing 'system.js' script tag (it wasn't present in the bundle)
	 and to reference the corrected 'ghost-system.js' filename.
3. Did NOT change the logic of ghost-system.js: it already calls the backend endpoint /api/chat.
4. Left ai.js in place but note: ai.js and ghost.js currently attempt to call OpenAI directly using
	 import.meta.env which does not work in a plain browser static context. Prefer backend proxy.

Important next steps (backend checks you must do):
- Check your Go backend handler for /api/chat. Ensure it reads OPENAI_API_KEY from the environment (Replit Secret)
	and forwards the request to OpenAI properly. If your backend returns the fixed string "i accept you", fix that code.
- Example Go handler (provided by assistant) is saved to 'GO_HANDLER_EXAMPLE.txt' in this zip.

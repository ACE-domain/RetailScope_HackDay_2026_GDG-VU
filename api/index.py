import os
import json
import base64  # <--- Added for image encoding
from fastapi import FastAPI, Form, Request, UploadFile, File  # <--- Added UploadFile and File
from fastapi.responses import HTMLResponse
from openai import OpenAI

app = FastAPI(title="Retail Stock")

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en" class="antialiased">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Retail Stock Audit | Enterprise Dashboard</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script>
        tailwind.config = {
            darkMode: 'media',
            theme: {
                extend: {
                    colors: {
                        primary: '#3b82f6',
                        secondary: '#1e293b',
                    }
                }
            }
        }
    </script>
</head>
<body class="bg-gray-50 dark:bg-gray-900 text-gray-800 dark:text-gray-100 min-h-screen p-4 md:p-8 font-sans">
    <div class="max-w-5xl mx-auto">
        <header class="mb-8">
            <h1 class="text-3xl font-bold text-gray-900 dark:text-white flex items-center gap-3">
                <svg class="w-8 h-8 text-blue-600 dark:text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-3 7h3m-3 4h3m-6-4h.01M9 16h.01"></path></svg>
                Retail Stock Audit
            </h1>
            <p class="text-gray-600 dark:text-gray-400 mt-2">AI-Powered Inventory Intelligence</p>
        </header>

        <main class="space-y-6">
            <div class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-6">
                <form id="auditForm" action="/api/audit" method="POST" enctype="multipart/form-data" class="space-y-4">
                    <div>
                        <label for="stockDetails" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Audit Details / Notes</label>
                        <textarea id="stockDetails" name="stock_details" rows="3" class="w-full rounded-lg bg-gray-50 dark:bg-gray-700 border border-gray-300 dark:border-gray-600 text-gray-900 dark:text-white p-3" placeholder="Describe the current state or upload a photo below..."></textarea>
                    </div>
    
    <!-- Shelf Photo Upload Field -->
                    <div>
                        <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Upload Shelf Photo (Optional)</label>
                        <input type="file" name="shelf_image" accept="image/*" class="w-full text-sm text-gray-500 dark:text-gray-400 file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:text-sm file:font-semibold file:bg-blue-600 file:text-white hover:file:bg-blue-700 cursor-pointer"/>
                    </div>

                    <button type="submit" class="inline-flex justify-center items-center py-2 px-6 border border-transparent shadow-sm text-sm font-medium rounded-lg text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500">
                    Run Audit Analysis
                </button>
            </form>
            </div>

            <div id="loading" class="hidden">
                <div class="flex items-center justify-center space-x-3 p-6 bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700">
                    <div class="w-6 h-6 border-4 border-blue-500 border-t-transparent rounded-full animate-spin"></div>
                    <span class="text-gray-600 dark:text-gray-400 font-medium">Processing retail data with Gemma 4...</span>
                </div>
            </div>

            <div id="error" class="hidden p-4 rounded-lg bg-red-50 dark:bg-red-900/30 border border-red-200 dark:border-red-800 text-red-700 dark:text-red-400 text-sm font-medium"></div>

            <div id="result" class="hidden space-y-6">
                <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
                    <h2 class="text-xl font-semibold text-gray-900 dark:text-white">Audit Report</h2>
                    <button id="exportBtn" class="inline-flex items-center px-4 py-2 border border-gray-300 dark:border-gray-600 shadow-sm text-sm font-medium rounded-lg text-gray-700 dark:text-gray-200 bg-white dark:bg-gray-700 hover:bg-gray-50 dark:hover:bg-gray-600 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition-colors">
                        <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"></path></svg>
                        Export Report
                    </button>
                </div>
            </div>
        </main>
    </div>

    <script>
        let currentAuditData = null;

        document.getElementById('auditForm').addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const details = document.getElementById('stockDetails').value;
            const submitBtn = e.target.querySelector('button');
            const loading = document.getElementById('loading');
            const resultDiv = document.getElementById('result');
            const errorDiv = document.getElementById('error');
            
            submitBtn.disabled = true;
            submitBtn.classList.add('opacity-50', 'cursor-not-allowed');
            loading.classList.remove('hidden');
            resultDiv.classList.add('hidden');
            errorDiv.classList.add('hidden');
            currentAuditData = null;
            
            try {
                const formElement = document.getElementById('auditForm');
                const formData = new FormData(formElement);
                
                const response = await fetch('/api/audit', {
                    method: 'POST',
                    body: formData
                });
                
                const data = await response.json();
                
                if (response.ok) {
                    currentAuditData = data;
                    document.getElementById('emptySlots').textContent = data.empty_slots_detected;
                    document.getElementById('shelfScore').textContent = data.shelf_organization_score;
                    
                    const populateList = (elementId, items) => {
                        const el = document.getElementById(elementId);
                        el.innerHTML = '';
                        if (items && items.length > 0) {
                            items.forEach(item => {
                                const li = document.createElement('li');
                                li.className = 'flex items-start gap-2';
                                li.innerHTML = `<svg class="w-5 h-5 text-gray-400 mt-0.5 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg> <span>${item}</span>`;
                                el.appendChild(li);
                            });
                        } else {
                            el.innerHTML = '<li class="text-gray-500 dark:text-gray-500 italic">None</li>';
                        }
                    };

                    populateList('urgentRestock', data.urgent_restock);
                    populateList('standardRestock', data.standard_restock);
                    
                    document.getElementById('purchaseOrder').textContent = data.purchase_order_email || 'No purchase order generated.';
                    
                    resultDiv.classList.remove('hidden');
                } else {
                    throw new Error(data.detail || 'An error occurred during the audit.');
                }
            } catch (err) {
                errorDiv.textContent = err.message;
                errorDiv.classList.remove('hidden');
            } finally {
                submitBtn.disabled = false;
                submitBtn.classList.remove('opacity-50', 'cursor-not-allowed');
                loading.classList.add('hidden');
            }
        });

        document.getElementById('copyPOBtn').addEventListener('click', () => {
            const poText = document.getElementById('purchaseOrder').textContent;
            navigator.clipboard.writeText(poText).then(() => {
                const btn = document.getElementById('copyPOBtn');
                const originalText = btn.innerHTML;
                btn.innerHTML = `<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path></svg> Copied!`;
                setTimeout(() => { btn.innerHTML = originalText; }, 2000);
            });
        });

        document.getElementById('exportBtn').addEventListener('click', () => {
            if (!currentAuditData) return;
            
            const d = currentAuditData;
            const report = `# Retail Stock Audit Report

## Summary
- **Empty Slots Detected:** ${d.empty_slots_detected}
- **Shelf Organization Score:** ${d.shelf_organization_score} / 10

## Priority Triage

### Urgent (High Revenue Impact)
${(d.urgent_restock || []).map(i => '- ' + i).join('\n') || 'None'}

### Standard Restock
${(d.standard_restock || []).map(i => '- ' + i).join('\n') || 'None'}

## Purchase Order Email

${d.purchase_order_email || ''}
`;
            const blob = new Blob([report], { type: 'text/markdown' });
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `retail-audit-${new Date().toISOString().slice(0,10)}.md`;
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            URL.revokeObjectURL(url);
        });
    </script>
</body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
async def read_root():
    return HTML_TEMPLATE

@app.post("/api/audit")
async def run_audit(
    stock_details: str = Form(""), shelf_image: UploadFile = File(None)
):
  api_key = os.environ.get("DO_INFERENCE_KEY")
  if not api_key:
    return {
        "detail": "DO_INFERENCE_KEY is not set in the environment variables."
    }, 500

  client = OpenAI(
      base_url="https://inference.do-ai.run/v1",
      api_key=api_key,
  )

  prompt = f"""
    You are an expert retail inventory and supermarket shelf auditor. Analyze the provided image of retail store shelves/racks and/or stock details.
    Look for disorganized products, misplaced items, or empty shelf slots.
    Extract or estimate the following information:
    1. 'empty_slots_detected': An estimate of empty shelf slots or missing products (integer).
    2. 'shelf_organization_score': A score out of 10 based on how neat and organized the retail shelves are (integer).
    3. 'urgent_restock': A list of items that are depleted or missing urgently.
    4. 'standard_restock': A list of items for standard restock.
    5. 'purchase_order_email': A formal, ready-to-send supplier purchase order email requesting the exact restocks needed for the store.
    6. 'organization_tips': A list of 3-4 actionable steps or tips for store workers on how to sort, group, and reorganize these shelves properly (list of strings).

    Return ONLY a valid JSON object with the exact keys: "empty_slots_detected", "shelf_organization_score", "urgent_restock" (list of strings), "standard_restock" (list of strings), "purchase_order_email" (string), "organization_tips" (list of strings).
    """

  # Build multimodal content payload supporting text, images, or both
  content_payload = [{
      "type": "text",
      "text": (
          prompt
          + f"\n\nWorker Notes: {stock_details if stock_details else 'None'}"
      ),
  }]

  if shelf_image and shelf_image.filename:
    image_bytes = await shelf_image.read()
    base64_image = base64.b64encode(image_bytes).decode("utf-8")
    content_payload.append({
        "type": "image_url",
        "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"},
    })

  try:
    response = client.chat.completions.create(
        model="gemma-4-31B-it",
        messages=[{"role": "user", "content": content_payload}],
        temperature=0.1,
    )

    result_text = response.choices[0].message.content.strip()

    if result_text.startswith("```json"):
      result_text = result_text[7:]
    if result_text.startswith("```"):
      result_text = result_text[3:]
    if result_text.endswith("```"):
      result_text = result_text[:-3]

    result_text = result_text.strip()
    audit_data = json.loads(result_text)

  except Exception as e:
    audit_data = {
        "empty_slots_detected": 0,
        "shelf_organization_score": 5,
        "urgent_restock": [],
        "purchase_order_email": f"Error parsing response: {str(e)}",
    }

  # Build the results HTML snippet including organization tips
  org_tips_html = "".join([f"<li class='flex items-start gap-2'><span class='text-blue-400 font-bold'>•</span><span>{tip}</span></li>" for tip in audit_data.get('organization_tips', [])])

  results_html = f"""
    <div class="mt-8 bg-gray-800 p-6 rounded-xl border border-gray-700 shadow-lg space-y-4">
        <h2 class="text-2xl font-bold text-blue-400">Audit Results & Triage</h2>
        <div class="grid grid-cols-2 gap-4">
            <div class="bg-gray-900 p-4 rounded border border-gray-700">
                <span class="text-gray-400 text-sm">Empty Slots Detected</span>
                <p class="text-3xl font-bold text-red-400">{audit_data.get('empty_slots_detected', 0)}</p>
            </div>
            <div class="bg-gray-900 p-4 rounded border border-gray-700">
                <span class="text-gray-400 text-sm">Organization Score</span>
                <p class="text-3xl font-bold text-green-400">{audit_data.get('shelf_organization_score', 0)}/10</p>
            </div>
        </div>
        <div class="bg-gray-900 p-4 rounded border border-gray-700">
            <h3 class="font-semibold text-gray-200 mb-2">Urgent Restock Items</h3>
            <p class="text-red-300">{', '.join(audit_data.get('urgent_restock', [])) if audit_data.get('urgent_restock') else 'None'}</p>
        </div>
        <div class="bg-gray-900 p-4 rounded border border-gray-700">
            <h3 class="font-semibold text-gray-200 mb-2">Shelf Reorganization & Merchandising Plan</h3>
            <ul class="space-y-2 text-gray-300 text-sm">{org_tips_html if org_tips_html else '<li class="text-gray-500 italic">No specific reorganization needed.</li>'}</ul>
        </div>
        <div class="bg-gray-900 p-4 rounded border border-gray-700">
            <h3 class="font-semibold text-gray-200 mb-2">Generated Purchase Order</h3>
            <pre class="whitespace-pre-wrap text-sm text-gray-300 bg-gray-950 p-3 rounded">{audit_data.get('purchase_order_email', '')}</pre>
        </div>
    </div>
    """
  # Unhide the results container and inject the content directly
  rendered = HTML_TEMPLATE.replace(
      'id="result" class="hidden space-y-6">',
      f'id="result" class="space-y-6">{results_html}',
  )

  return HTMLResponse(content=rendered, status_code=200)
    
/**
 * Very lightweight markdown-to-HTML renderer for chat bubbles.
 * Handles: **bold**, *italic*, numbered lists, bullet lists, line breaks.
 */
export function formatMessage(text) {
  if (!text) return '';

  let html = text
    // Escape HTML
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    // Bold
    .replace(/\*\*(.+?)\*\*/g, '<strong class="text-emerald-300 font-semibold">$1</strong>')
    // Italic
    .replace(/\*(.+?)\*/g, '<em class="text-slate-300">$1</em>')
    // Numbered list items
    .replace(/^\s*(\d+)\.\s+(.+)$/gm, '<li class="ml-4 list-decimal">$2</li>')
    // Bullet list items
    .replace(/^\s*[-•]\s+(.+)$/gm, '<li class="ml-4 list-disc">$1</li>')
    // Newlines to <br>
    .replace(/\n/g, '<br/>');

  return html;
}

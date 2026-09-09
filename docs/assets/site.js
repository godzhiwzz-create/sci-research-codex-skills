"use strict";

// Progressive enhancement: the commands remain selectable when scripting or clipboard access is unavailable.
const copyStatus = document.getElementById("copy-status");
document.querySelectorAll("[data-copy]").forEach((button) => {
  const command = document.getElementById(button.dataset.copy);
  if (!command || !copyStatus) return;
  button.hidden = false;
  button.addEventListener("click", async () => {
    button.disabled = true;
    try {
      if (!navigator.clipboard || !window.isSecureContext) throw new Error("Clipboard unavailable");
      await navigator.clipboard.writeText(command.textContent);
      copyStatus.textContent = "已复制。请在终端核对后手动运行；网页不会执行命令。";
    } catch {
      copyStatus.textContent = "浏览器未允许复制。请直接选择上面的命令，手动复制。";
      command.closest("pre").focus();
    } finally {
      button.disabled = false;
    }
  });
});

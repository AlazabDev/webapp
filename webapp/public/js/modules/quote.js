
// Requires: https://cdn.jsdelivr.net/npm/emailjs-com@3/dist/email.min.js
// Configure your keys:
const EMAILJS_PUBLIC_KEY = "YOUR_PUBLIC_KEY";
const EMAILJS_SERVICE_ID  = "YOUR_SERVICE_ID";
const EMAILJS_TEMPLATE_ID = "YOUR_TEMPLATE_ID";

document.addEventListener('DOMContentLoaded', () => {
  if(window.emailjs){
    emailjs.init(EMAILJS_PUBLIC_KEY);
  }
  const form = document.getElementById('quote-form');
  const status = document.getElementById('quote-status');

  if(!form) return;

  form.addEventListener('submit', async (e)=>{
    e.preventDefault();
    status.textContent = (document.documentElement.dir === 'rtl')
      ? 'جاري الإرسال...'
      : 'Sending...';

    try{
      if(!window.emailjs) throw new Error('EmailJS not loaded');
      // You can use sendForm to auto-capture fields:
      const res = await emailjs.sendForm(EMAILJS_SERVICE_ID, EMAILJS_TEMPLATE_ID, form);
      status.textContent = (document.documentElement.dir === 'rtl')
        ? 'تم الإرسال بنجاح. سنتواصل معك قريبًا.'
        : 'Sent successfully. We will contact you soon.';
      form.reset();
    }catch(err){
      console.error(err);
      status.textContent = (document.documentElement.dir === 'rtl')
        ? 'حدث خطأ أثناء الإرسال. حاول مرة أخرى.'
        : 'Error while sending. Please try again.';
    }
  });
});

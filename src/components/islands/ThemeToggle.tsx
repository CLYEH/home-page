import { useEffect, useState } from 'react';

// 全站少數的 React island：light/dark 切換。掛載方式：<ThemeToggle client:idle />
export default function ThemeToggle() {
  const [dark, setDark] = useState(false);

  useEffect(() => {
    setDark(document.documentElement.classList.contains('dark'));
  }, []);

  const toggle = () => {
    const next = !dark;
    setDark(next);
    document.documentElement.classList.toggle('dark', next);
    localStorage.setItem('theme', next ? 'dark' : 'light');
  };

  return (
    <button
      type="button"
      onClick={toggle}
      aria-label="切換深淺色主題"
      aria-pressed={dark}
      className="rounded-md border border-border px-md py-sm text-label-md text-on-surface hover:border-primary dark:border-border-dark dark:text-on-surface-dark dark:hover:border-primary-bright"
    >
      {dark ? 'Light' : 'Dark'}
    </button>
  );
}

// components/SpaPageView.tsx
'use client';
import { useEffect } from 'react';

export default function SpaPageView() {
  useEffect(() => {
    window.dataLayer?.push({
      event: 'page_view',
      page_path: window.location.pathname,
      page_location: window.location.href,
    });
  }, []);

  return null; // 화면에는 아무 것도 렌더링하지 않음 > UI 없음, 이벤트만 전송
}
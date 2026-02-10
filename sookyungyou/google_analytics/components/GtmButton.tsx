'use client';

declare global {
    interface Window {
        dataLayer?: any[];
    }
}

export default function GtmButton() {
    // 트리거
    const handleClick = () => {
        // window.dataLayer <- GTM, GA4에 붙어서 데이터 수집하는 파트
        // event로 button_click <- 미리보기에서 이벤트로 나타났던 이름
        window.dataLayer?.push({ event: 'button_click', button_name: 'test_button' });
        alert('button_click 이벤트 전송 완료!');
    };

    return (
        // className은 꾸미는 것 (tailwindcss)
        // onClick = {트리거}
        // 버튼은 뭐다?
        // 1. 기획/마케팅 관점: 사용자의 행위 관측 장치
        // 2. 개발자 관점: 트리거 (클릭 시 백엔드로 데이터 보내거나, GA4로 데이터 보냄)
        // handleClick 이 버튼 클릭 시 동작할 트리거
        <button
            onClick={handleClick}
            className="flex h-12 w-full items-center justify-center rounded-full bg-blue-600 px-5 text-white transition-colors hover:bg-blue-700 md:w-[200px]"
        >
            GA4 버튼 (관측 장치)
        </button>
    );
}
(globalThis.TURBOPACK || (globalThis.TURBOPACK = [])).push([typeof document === "object" ? document.currentScript : undefined,
"[project]/components/GtmButton.tsx [app-client] (ecmascript)", ((__turbopack_context__) => {
"use strict";

__turbopack_context__.s([
    "default",
    ()=>GtmButton
]);
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/node_modules/next/dist/compiled/react/jsx-dev-runtime.js [app-client] (ecmascript)");
'use client';
;
function GtmButton() {
    // 트리거
    const handleClick = ()=>{
        // window.dataLayer <- GTM, GA4에 붙어서 데이터 수집하는 파트
        // event로 button_click <- 미리보기에서 이벤트로 나타났던 이름
        window.dataLayer?.push({
            event: 'button_click',
            button_name: 'test_button'
        });
        alert('button_click 이벤트 전송 완료!');
    };
    return(// className은 꾸미는 것 (tailwindcss)
    // onClick = {트리거}
    // 버튼은 뭐다?
    // 1. 기획/마케팅 관점: 사용자의 행위 관측 장치
    // 2. 개발자 관점: 트리거 (클릭 시 백엔드로 데이터 보내거나, GA4로 데이터 보냄)
    // handleClick 이 버튼 클릭 시 동작할 트리거
    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("button", {
        onClick: handleClick,
        className: "flex h-12 w-full items-center justify-center rounded-full bg-blue-600 px-5 text-white transition-colors hover:bg-blue-700 md:w-[200px]",
        children: "GA4 버튼 (관측 장치)"
    }, void 0, false, {
        fileName: "[project]/components/GtmButton.tsx",
        lineNumber: 25,
        columnNumber: 9
    }, this));
}
_c = GtmButton;
var _c;
__turbopack_context__.k.register(_c, "GtmButton");
if (typeof globalThis.$RefreshHelpers$ === 'object' && globalThis.$RefreshHelpers !== null) {
    __turbopack_context__.k.registerExports(__turbopack_context__.m, globalThis.$RefreshHelpers$);
}
}),
"[project]/components/SpaPageView.tsx [app-client] (ecmascript)", ((__turbopack_context__) => {
"use strict";

// components/SpaPageView.tsx
__turbopack_context__.s([
    "default",
    ()=>SpaPageView
]);
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/node_modules/next/dist/compiled/react/index.js [app-client] (ecmascript)");
var _s = __turbopack_context__.k.signature();
'use client';
;
function SpaPageView() {
    _s();
    (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useEffect"])({
        "SpaPageView.useEffect": ()=>{
            window.dataLayer?.push({
                event: 'page_view',
                page_path: window.location.pathname,
                page_location: window.location.href
            });
        }
    }["SpaPageView.useEffect"], []);
    return null; // 화면에는 아무 것도 렌더링하지 않음 > UI 없음, 이벤트만 전송
}
_s(SpaPageView, "OD7bBpZva5O2jO+Puf00hKivP7c=");
_c = SpaPageView;
var _c;
__turbopack_context__.k.register(_c, "SpaPageView");
if (typeof globalThis.$RefreshHelpers$ === 'object' && globalThis.$RefreshHelpers !== null) {
    __turbopack_context__.k.registerExports(__turbopack_context__.m, globalThis.$RefreshHelpers$);
}
}),
]);

//# sourceMappingURL=components_408b488e._.js.map
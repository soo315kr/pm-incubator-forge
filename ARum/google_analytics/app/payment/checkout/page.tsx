"use client";

import { loadTossPayments, ANONYMOUS } from "@tosspayments/tosspayments-sdk";
import { useEffect, useState } from "react";

const clientKey = process.env.NEXT_PUBLIC_TOSS_CLIENT_KEY!;
const customerKey = ANONYMOUS; // 비회원 결제, 회원이면 실제 customerKey

export default function CheckoutPage() {
    const [amount, setAmount] = useState({ currency: "KRW", value: 50000 });
    const [ready, setReady] = useState(false);
    const [widgets, setWidgets] = useState<any>(null);

    // 결제 위젯 초기화
    useEffect(() => {
        async function fetchPaymentWidgets() {
            const tossPayments = await loadTossPayments(clientKey);
            const widgets = tossPayments.widgets({ customerKey });
            setWidgets(widgets);
        }
        fetchPaymentWidgets();
    }, []);

    // 위젯 렌더링
    useEffect(() => {
        if (!widgets) return;

        async function render() {
            await widgets.setAmount(amount);

            await Promise.all([
                widgets.renderPaymentMethods({
                    selector: "#payment-method",
                    variantKey: "DEFAULT",
                }),
                widgets.renderAgreement({
                    selector: "#agreement",
                    variantKey: "AGREEMENT",
                }),
            ]);

            setReady(true);
        }

        render();
    }, [widgets, amount]);

    return (
        <div className="wrapper p-8">
            <h1 className="text-2xl font-bold mb-4">프리미엄 구독 결제</h1>
            <div id="payment-method" className="mb-4" />
            <div id="agreement" className="mb-4" />

            {/* 쿠폰 체크박스 */}
            <label>
                <input
                    type="checkbox"
                    disabled={!ready}
                    onChange={(e) =>
                        setAmount((prev) => ({
                            ...prev,
                            value: e.target.checked ? prev.value - 5000 : prev.value + 5000,
                        }))
                    }
                />
                5,000원 쿠폰 적용
            </label>

            {/* 결제 버튼 */}
            <button
                disabled={!ready}
                className="bg-green-500 px-6 py-2 mt-4 text-white rounded hover:bg-green-600"
                onClick={async () => {
                    if (!widgets) return;

                    try {
                        await widgets.requestPayment({
                            orderId: `sub_${Date.now()}`,
                            orderName: "프리미엄 구독",
                            successUrl: window.location.origin + "/payment/success",
                            failUrl: window.location.origin + "/payment/fail",
                            customerEmail: "customer@example.com",
                            customerName: "김토스",
                            customerMobilePhone: "01012341234",
                        });
                    } catch (err) {
                        console.error("결제창 호출 중 오류:", err);
                    }
                }}
            >
                결제하기
            </button>
        </div>
    );
}

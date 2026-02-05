"use client";

export default function PaymentPage() {
    const requestPayment = async () => {
        const tossPayments = (window as any).TossPayments(
            process.env.NEXT_PUBLIC_TOSS_CLIENT_KEY
        );

        await tossPayments.requestPayment("카드", {
            amount: 10000,
            orderId: `order_${Date.now()}`,
            orderName: "결제 테스트",
            customerName: "전도사",
            successUrl: `${process.env.NEXT_PUBLIC_BASE_URL}/payment/success`,
            failUrl: `${process.env.NEXT_PUBLIC_BASE_URL}/payment/fail`,
        });
    };

    return (
        <button onClick={requestPayment} className="px-4 py-2 bg-blue-500 text-white">
            토스 결제하기
        </button>
    );
}

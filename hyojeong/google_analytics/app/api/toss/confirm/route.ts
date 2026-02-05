import { NextResponse } from "next/server";

export async function POST(req: Request) {
    const { paymentKey, orderId, amount } = await req.json();

    const response = await fetch(
        "https://api.tosspayments.com/v1/payments/confirm",
        {
            method: "POST",
            headers: {
                Authorization:
                    "Basic " +
                    Buffer.from(process.env.TOSS_SECRET_KEY + ":").toString("base64"),
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                paymentKey,
                orderId,
                amount,
            }),
        }
    );

    const data = await response.json();

    if (!response.ok) {
        return NextResponse.json(data, { status: 400 });
    }

    // 여기서 DB 저장, 구독 처리, 아이템 지급 등 진행
    return NextResponse.json({ success: true, data });
}

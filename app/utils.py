import random

from app.semtiment_analysis import predict_sentiment

def count_cart(cart):
    total_quantity, total_amount = 0, 0
    if cart:
        for c in cart.values():
            total_quantity += c['quantity']
            total_amount += c['quantity'] * c['price']
    return {
        "total_quantity": total_quantity,
        "total_amount": total_amount
    }


def get_reply_content(review):
    positive_replies = [
        "Rất vui khi bạn hài lòng với sản phẩm của chúng mình!",
        "Cảm ơn bạn rất nhiều vì đã để lại đánh giá tuyệt vời này. Chúng mình rất vui khi bạn hài lòng với sản phẩm của chúng mình.",
        "Chúng mình rất biết ơn những lời khen của bạn. Đó là niềm vinh dự của chúng tôi khi được phục vụ bạn.",
        "Thật tuyệt vời khi nghe bạn thích sản phẩm của chúng mình. Cảm ơn bạn đã chia sẻ trải nghiệm của bạn với chúng mình.",
        "Cảm ơn bạn vì đã chọn chúng mình"
    ]

    negative_replies = [
        "Cảm ơn bạn đã đóng góp ý kiến cho shop, shop sẽ hõ trợ bạn trong giây lát và sẽ cải thiện trong tương lai."
    ]
    is_positive = predict_sentiment(review)
    if is_positive:
        return random.choice(positive_replies)
    else:
        return random.choice(negative_replies)
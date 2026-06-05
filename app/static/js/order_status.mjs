export default class OrderStatus {
	static CREATED = 'CREATED';
	static CONFIRMED = 'CONFIRMED';
	static IN_TRANSIT = 'IN_TRANSIT';
	static DELIVERED = 'DELIVERED';
	static CANCELLED = 'CANCELLED';

	static ValueToStr(statusValue) {
		switch (statusValue) {
			case 'CREATED': return 'Создан';
			case 'CONFIRMED': return 'Подтверждён';
			case 'IN_TRANSIT': return 'В пути';
			case 'DELIVERED': return 'Завершён';
			case 'CANCELLED': return 'Отменён';
			default: return 'Неизвестно';
		}
	}

	static StrToColor(statusStr) {
		let lower = statusStr.toLowerCase();
		if (lower == 'создан') return `#663300`;
		else if (lower == 'подтверждён') return `#66FF00`;
		else if (lower == 'в пути') return `#0033FF`;
		else if (lower == 'завершён') return `#33CCFF`;
		else if (lower == 'отменён') return `#FF3300`;
		return `gray`;
	}
};

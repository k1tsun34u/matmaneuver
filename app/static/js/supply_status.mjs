export default class SupplyStatus {
	static CREATED = 'CREATED';
	static CONFIRMED = 'CONFIRMED';
	static IN_TRANSIT = 'IN_TRANSIT';
	static DELIVERED = 'DELIVERED';
	static CANCELLED = 'CANCELLED';

	static ValueToStr(statusValue) {
		switch (statusValue) {
			case 'CREATED': return 'Создана';
			case 'CONFIRMED': return 'Подтверждена';
			case 'IN_TRANSIT': return 'В пути';
			case 'DELIVERED': return 'Завершена';
			case 'CANCELLED': return 'Отменена';
			default: return 'Неизвестно';
		}
	}

	static StrToColor(statusStr) {
		let lower = statusStr.toLowerCase();
		if (lower == 'создана') return `#663300`;
		else if (lower == 'подтверждена') return `#66FF00`;
		else if (lower == 'в пути') return `#0033FF`;
		else if (lower == 'завершена') return `#33CCFF`;
		else if (lower == 'отменена') return `#FF3300`;
		return `gray`;
	}
};

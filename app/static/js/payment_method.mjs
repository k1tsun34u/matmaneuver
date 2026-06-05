export default class PaymentMethod {
	static CARD = 'CARD';
	static CASH = 'CASH';
	static SBP = 'SBP';

	static ValueToStr(methodValue) {
		switch (methodValue) {
			case 'CARD': return 'Банковская карта';
			case 'CASH': return 'Наличные';
			case 'SBP': return 'СБП';
			default: return 'Неизвестен';
		}
	}

	static StrToColor(methodStr) {
		let lower = methodStr.toLowerCase();
		if (lower == 'банковская карта') return `#FF7F50`;
		else if (lower == 'наличные') return `#006400`;
		else if (lower == 'сбп') return `#00BFFF`;
		return `gray`;
	}
};

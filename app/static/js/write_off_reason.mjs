export default class WriteOffReason {
	static EXPIRED = "EXPIRED";
	static DAMAGED = "DAMAGED";
	static LOST = "LOST";
	static STOLEN = "STOLEN";
	static INVENTORY_MISMATCH = "INVENTORY_MISMATCH";
	static OTHER = "OTHER";

	static ValueToStr(value) {
		switch (value) {
			case WriteOffReason.EXPIRED: return 'Истёк срок годности товара';
			case WriteOffReason.DAMAGED: return 'Товар повреждён';
			case WriteOffReason.LOST: return 'Товар утерян';
			case WriteOffReason.STOLEN: return 'Товар украден';
			case WriteOffReason.INVENTORY_MISMATCH: return 'Товар перепутан';
			case WriteOffReason.OTHER: return 'Другая';
		}

		return 'Неизвестна';
	}
};

export default class DateConv {
	static DateTimeToStr(date) {
		return new Date(date).toISOString().slice(0, 19).replace('T', ' ');
	}
};
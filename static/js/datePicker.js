  document.addEventListener("alpine:init", () => {
    Alpine.data("datePicker", () => ({
      selectedDate: '',
      showDate: new Date(),
      open: false,
      weekDays: ['Пн','Вт','Ср','Чт','Пт','Сб','Вс'],
      monthNames: ['Январь','Февраль','Март','Апрель','Май','Июнь','Июль','Август','Сентябрь','Октябрь','Ноябрь','Декабрь'],

      get showMonthYear(){
        return this.monthNames[this.showDate.getMonth()] + ', ' + this.showDate.getFullYear()
      },
      datePick(row, col){
        const date = this.cellDate(row, col)
        this.selectedDate = `${date.getDate()}/${date.getMonth() + 1}/${date.getFullYear()}`;

      },
      offsetMonth(offset){
        this.showDate = new Date(
          this.showDate.getFullYear(),
          this.showDate.getMonth() + offset,
          1
        )
      },
      curMonthStartDay(){
         const day = new Date(
          this.showDate.getFullYear(),
          this.showDate.getMonth(),
          1
        ).getDay()
        return day + ( day === 0 ? 6 : -1 )

      },
      cellDate(row,col){
        const day = (row-1)*7 + col - this.curMonthStartDay()
        return new Date(
          this.showDate.getFullYear(),
          this.showDate.getMonth(),
          day
        )
      },
      cellDay(row, col){
        return this.cellDate(row, col).getDate()

      },
      curMonthWeeks(){
        const daysInMonth = new Date(
          this.showDate.getFullYear(),
          this.showDate.getMonth(),
          0
        ).getDate()
        return Math.ceil((daysInMonth + this.curMonthStartDay()) / 7)
      },
    }));
  });
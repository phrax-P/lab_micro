/*
 * This file is part of the libopencm3 project.
 *
 * Copyright (C) 2014 Chuck McManis <cmcmanis@mcmanis.com>
 *
 * This library is free software: you can redistribute it and/or modify
 * it under the terms of the GNU Lesser General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This library is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU Lesser General Public License for more details.
 *
 * You should have received a copy of the GNU Lesser General Public License
 * along with this library.  If not, see <http://www.gnu.org/licenses/>.
 */

#include <stdint.h>
#include <stdio.h>
#include <math.h>
#include "clock.h"
#include "console.h"
#include "sdram.h"
#include "lcd-spi.h"
#include "gfx.h"
#include "spi_gyro.h"
#include "gfx.h"
#include <libopencm3/stm32/rcc.h>
#include <libopencm3/stm32/gpio.h>
#include <libopencm3/stm32/spi.h>
#include <libopencm3/stm32/usart.h> 
#include <libopencm3/stm32/adc.h>
#include <libopencm3/cm3/nvic.h>

void setup();
void init_message();
void print_axes(struct axis axes);

/*
 * This is our example, the heavy lifing is actually in lcd-spi.c but
 * this drives that code.
 */


int main(void)
{
	clock_setup();
	console_setup(115200);
	sdram_init();
	setup();
	lcd_spi_init();

	init_message();
	struct axis lecturas;

	while(1){
		lecturas = read_axis();
		print_axes(lecturas);
	}
	

	return 0;
}

void setup(){
	setup_spi();

	gpio_clear(GPIOC, GPIO1);
	spi_send(SPI5, GYR_CTRL_REG1); 
	spi_read(SPI5);
	spi_send(SPI5, GYR_CTRL_REG1_PD | GYR_CTRL_REG1_XEN |
			GYR_CTRL_REG1_YEN | GYR_CTRL_REG1_ZEN |
			(3 << GYR_CTRL_REG1_BW_SHIFT));
	spi_read(SPI5);
	gpio_set(GPIOC, GPIO1); 

    gpio_clear(GPIOC, GPIO1);
	spi_send(SPI5, GYR_CTRL_REG4);
	spi_read(SPI5);
	spi_send(SPI5, (1 << GYR_CTRL_REG4_FS_SHIFT));
	spi_read(SPI5);
	gpio_set(GPIOC, GPIO1);
	
}

void init_message(){
	console_puts("LCD Initialized\n");
	console_puts("Should have a checker pattern, press any key to proceed\n");
	msleep(2000);
/*	(void) console_getc(1); */
	gfx_init(lcd_draw_pixel, 240, 320);
	gfx_fillScreen(LCD_GREY);
	gfx_fillRoundRect(10, 10, 220, 220, 5, LCD_WHITE);
	gfx_setCursor(15, 25);
	gfx_setTextSize(2);
	gfx_puts("BIENVENIDO A");
	gfx_setTextSize(2);
	gfx_setCursor(15, 55);
	gfx_puts("SISMOGRAFO");
	gfx_setTextSize(1);
	gfx_setCursor(15, 85);
	gfx_puts("AUTORES:");
	gfx_setCursor(15, 115);
	gfx_puts("Oscar Fallas - B92861");
	gfx_setCursor(15, 145);
	gfx_puts("Kenny Wu - C01111");
	lcd_show_frame();
	console_puts("Now it has a bit of structured graphics.\n");
	console_puts("Press a key for some simple animation.\n");
	msleep(8000);
}

void print_axes(struct axis axes){
	//Conversion de int a str
	char X[20], Y[20], Z[20];

	sprintf(X, "%d", axes.x);
	sprintf(Y, "%d", axes.y);
	sprintf(Z, "%d", axes.z);

	gfx_init(lcd_draw_pixel, 240, 320);
	gfx_fillScreen(LCD_GREY);
	gfx_fillRoundRect(10, 10, 220, 220, 5, LCD_WHITE);
	gfx_setCursor(15, 25);
	gfx_setTextSize(2);
	gfx_puts("LECTURAS: ");
	gfx_setTextSize(2);
	gfx_setCursor(15, 85);
	gfx_puts("X : ");
	gfx_setCursor(100, 85);
	gfx_puts(X);
	gfx_setTextSize(2);
	gfx_setCursor(15, 115);
	gfx_puts("Y : ");
	gfx_setCursor(100, 115);
	gfx_puts(Y);
	gfx_setCursor(15, 145);
	gfx_puts("Z : ");
	gfx_setCursor(100, 145);
	gfx_puts(Z);
	lcd_show_frame();
}

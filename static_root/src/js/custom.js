/**
 * Created by igor on 26.10.15.
 */

hs.graphicsDir = '/static_root/src/highslide/graphics/';
hs.align = 'center';
hs.transitions = ['expand', 'crossfade'];
hs.outlineType = 'rounded-white';
hs.fadeInOut = true;
//hs.dimmingOpacity = 0.75;

hs.lang = {
    cssDirection:     'ltr',
    loadingText :     'Ожидание...',
    loadingTitle :    'Нажмите, чтобы отменить',
    focusTitle :      'Нажмите, чтобы выдвинуть на',
    fullExpandTitle : 'Развернуть до исходного размера',
    fullExpandText :  'Полный экран',
    creditsText :     'Работает на Highslide JS',
    creditsTitle :    'Перейдите на главную страницу Highslide JS',
    previousText :    'Предыдущий',
    previousTitle :   'Предыдущие (стрелка влево)',
    nextText :        'Следующий',
    nextTitle :       'Дальше (стрелка вправо)',
    moveTitle :       'Двигаться',
    moveText :        'Двигаться',
    closeText :       'Закрывать',
    closeTitle :      'Закрыть (Esc)',
    resizeTitle :     'Размер восстановление',
    playText :        'Играть',
    playTitle :       'Воспроизвести слайд-шоу (пробел)',
    pauseText :       'Пауза',
    pauseTitle :      'Пауза слайд-шоу (пробел)',
    number :          'Изображение 1 2',
    restoreTitle :    'Нажмите, чтобы закрыть изображения, нажмите и удерживайте, чтобы перетащить. Используйте стрелки для движения вперед и назад.'
};

// Add the controlbar
hs.addSlideshow({
	//slideshowGroup: 'group1',
	interval: 5000,
	repeat: false,
	useControls: true,
	fixedControls: 'fit',
	overlayOptions: {
		opacity: 0.75,
		position: 'bottom center',
		hideOnMouseOut: true
	}
});

$(':checkbox').checkboxpicker();
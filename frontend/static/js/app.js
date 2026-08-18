document.addEventListener('DOMContentLoaded', () => {
    const toastContainer = document.getElementById('toast-container');
    window.showToast = function (message, type = 'info') {
        const toast = document.createElement('div');
        toast.className = `toast toast-${type}`;
        toast.textContent = message;
        toastContainer.appendChild(toast);
        setTimeout(() => toast.remove(), 3000);
    };

    const translations = {
        en: {
            brand_title: 'SmartMed Companion',
            brand_subtitle: 'Multimodal Prescription & Medication Safety Assistant',
            brand_title_short: 'SmartMed',
            brand_title_suffix: 'Companion',
            dashboard: 'Dashboard',
            prescriptions: 'Prescription Scanner',
            medicines: 'Medicines',
            reminders: 'Reminders',
            safety: 'Safety',
            emergency: 'Emergency',
            settings: 'Settings',
            search: 'Search',
            notifications: 'Notifications',
            profile_title: 'Your profile',
            full_name_field: 'Full name',
            username_field: 'Username',
            save_profile_button: 'Save profile',
            notification_title: 'Notifications',
            no_notifications: 'No new notifications.',
            view_reminders: 'View reminders',
            profile: 'Profile',
            good_evening: 'Good Evening',
            demo_mode: 'Demo mode',
            todays_medicines: "Today's medicines",
            active_prescriptions: '{count} active prescriptions',
            upcoming_reminders: 'Upcoming reminders',
            next_scheduled_reminder: 'Next scheduled reminder',
            safety_alerts: 'Safety alerts',
            review_instructions: 'Review instructions',
            recent_prescriptions: 'Recent prescriptions',
            stored_records: 'Stored records',
            todays_medicines_panel: "Today's medicines",
            active_status: 'Active',
            edit_button: 'Edit',
            delete_button: 'Delete',
            upcoming_reminders_panel: 'Upcoming reminders',
            recent_prescriptions_panel: 'Recent prescriptions',
            safety_alerts_panel: 'Safety alerts',
            medication_schedule: 'Medication schedule',
            reminders_page_title: 'Reminders',
            add_reminder_button: 'Add reminder',
            medicine_name_field: 'Medicine name',
            time_field: 'Time',
            frequency_field: 'Frequency',
            notes_field: 'Notes',
            save_reminder_button: 'Save reminder',
            cancel_button: 'Cancel',
            save_changes_button: 'Save changes',
            no_medicines_added: 'No medicines added yet.',
            no_reminders_scheduled: 'No reminders scheduled.',
            no_prescriptions_uploaded: 'No prescriptions uploaded yet.',
            no_safety_warnings: 'No safety warnings at this time.',
            table_name: 'Name',
            created_date: 'Created date',
            actions: 'Actions',
            no_medicines_yet: 'No medicines yet. Add a medicine from a prescription or manual entry.',
            medication_list: 'Medication list',
            medicines_page_title: 'Medicines',
            add_medicine_button: 'Add medicine',
            strength_field: 'Strength',
            duration_field: 'Duration',
            instructions_field: 'Instructions',
            source_field: 'Source',
            save_medicine_button: 'Save medicine',
            disclaimer: 'SmartMed Companion is an educational and medication-support tool. It does not replace advice, diagnosis, or treatment from a doctor or pharmacist.',
            prescription_intake: 'Prescription intake',
            prescription_scanner_title: 'Prescription scanner',
            upload_prescription: 'Upload prescription image or PDF',
            drag_drop_instruction: 'Drag and drop a file or select one from your device.',
            choose_file: 'Choose file',
            scan_extract: 'Scan & extract',
            remove_file: 'Remove',
            ocr_result: 'OCR result',
            waiting_for_file: 'Waiting for file',
            no_prescription_scanned: 'No prescription scanned yet.',
            confirm_extracted_details: 'Confirm extracted details',
            confirm_and_save: 'Confirm and save',
            medication_safety: 'Medication safety',
            safety_check: 'Safety check',
            safety_review: 'Safety review',
            no_safety_alerts: 'No safety alerts found.',
            urgent_help: 'Urgent help',
            emergency_info_title: 'Emergency and safety information',
            emergency_warning: 'If you are experiencing a serious or life-threatening reaction, seek immediate professional/emergency medical help.',
            emergency_note: 'Do not attempt self-diagnosis or medication changes without speaking to a qualified healthcare professional.',
            emergency_list_breathing: 'Difficulty breathing',
            emergency_list_swelling: 'Severe swelling',
            emergency_list_unconscious: 'Loss of consciousness',
            emergency_list_chest_pain: 'Severe chest pain',
            emergency_list_confusion: 'Severe confusion',
            emergency_list_allergy: 'Serious allergic reaction symptoms',
        },
        te: {
            brand_title_short: 'స్మార్ట్‌మెడ్',
            brand_title_suffix: 'కంపానియన్',
            brand_title: 'స్మార్ట్‌మెడ్',
            brand_subtitle: 'మల్టీమోడల్ ప్రిస్క్రిప్షన్ & మెడికేషన్ సేఫ్టీ అసిస్టెంట్',
            dashboard: 'డాష్‌బోర్డ్',
            prescriptions: 'ప్రిస్క్రిప్షన్ స్కానర్',
            medicines: 'మందులు',
            reminders: 'రిమైండర్లు',
            safety: 'సురక్ష',
            emergency: 'అత్యవసరం',
            settings: 'సెట్టింగ్స్',
            search: 'శోధించు',
            notifications: 'నోటిఫికేషన్లు',
            profile_title: 'మీ ప్రొఫైల్',
            full_name_field: 'పూర్తి పేరు',
            username_field: 'వినియోగదారు పేరు',
            save_profile_button: 'ప్రొఫైల్ సేవ్ చేయండి',
            notification_title: 'నోటిఫికేషన్లు',
            no_notifications: 'కొత్త నోటిఫికేషన్లు లేవు.',
            view_reminders: 'రిమైండర్లను చూడండి',
            profile: 'ప్రొఫైల్',
            good_evening: 'శుభ సాయంత్రం',
            demo_mode: 'డెమో మోడ్',
            todays_medicines: 'ఈరోజు మందులు',
            active_prescriptions: '{count} క్రియాశీల రెసిప్షన్లు',
            upcoming_reminders: 'వచ్చే రిమైండర్లు',
            next_scheduled_reminder: 'చెందిన తదుపరి రిమైండర్',
            safety_alerts: 'సేఫ్టీ అల్లర్ట్స్',
            review_instructions: 'ఇన్‌స్ట్రక్షన్లు చూడండి',
            recent_prescriptions: 'ఇటీవలి రెసిప్షన్లు',
            stored_records: 'సేవ్ చేసిన రికార్డులు',
            todays_medicines_panel: 'ఈరోజు మందులు',
            active_status: 'క్రియాశీలం',
            edit_button: 'సవరించు',
            delete_button: 'తొలగించు',
            upcoming_reminders_panel: 'వచ్చే రిమైండర్లు',
            recent_prescriptions_panel: 'ఇటీవలి రెసిప్షన్లు',
            safety_alerts_panel: 'సేఫ్టీ అల్లర్ట్స్',
            medication_schedule: 'మందు షెడ్యూల్',
            reminders_page_title: 'రిమైండర్లు',
            add_reminder_button: 'రిమైండర్ జోడించు',
            medicine_name_field: 'మందు పేరు',
            time_field: 'సమయం',
            frequency_field: 'తరచుదనం',
            notes_field: 'గమనికలు',
            save_reminder_button: 'రిమైండర్ సేవ్ చేయండి',
            cancel_button: 'రద్దు',
            save_changes_button: 'మార్పులను సేవ్ చేయండి',
            no_medicines_added: 'ఇంకా మందులు జోడించబడలేదు.',
            no_reminders_scheduled: 'షెడ్యూల్ చేయబడిన రిమైండర్లు లేవు.',
            no_prescriptions_uploaded: 'ఇంకా ప్రిస్క్రిప్షన్లు అప్లోడ్ కాలేదు.',
            no_safety_warnings: 'ఇప్పటికీ సేఫ్టీ వార్నింగ్లు లేవు.',
            table_name: 'పేరు',
            created_date: 'సృష్టించిన తేదీ',
            actions: 'చర్యలు',
            no_medicines_yet: 'ఇప్పటికీ మందులు లేవు. ప్రిస్క్రిప్షన్ లేదా మాన్యువల్ ఎంట్రీ ద్వారా జోడించండి.',
            medication_list: 'మందుల జాబితా',
            medicines_page_title: 'మందులు',
            add_medicine_button: 'మందు జోడించు',
            strength_field: 'శక్తి',
            duration_field: 'వ్యవధి',
            instructions_field: 'సూచనలు',
            source_field: 'మూలం',
            save_medicine_button: 'మందు సేవ్ చేయండి',
            disclaimer: 'SmartMed Companion విద్యాపరమైన మరియు మందు సహాయక సాధనం. ఇది వైద్యుడి లేదా ఫార్మిస్ట్‌ నుండి సూచనలు, నిర్ధారణ లేదా చికిత్సను భర్తీ చేయదు.',
            prescription_intake: 'ప్రిస్క్రిప్షన్ ఇన్‌టేక్',
            prescription_scanner_title: 'ప్రిస్క్రిప్షన్ స్కానర్',
            upload_prescription: 'ప్రిస్క్రిప్షన్ ఇమేజ్ లేదా PDF అప్లోడ్ చేయండి',
            drag_drop_instruction: 'ఫైల్‌ను ఇక్కడ డ్రాగ్ చేసి ఉంచండి లేదా మీ పరికరం నుండి ఎంచుకోండి.',
            choose_file: 'ఫైల్ ఎంపిక',
            scan_extract: 'స్కాన్ & ఎక్స్‌ట్రాక్ట్',
            remove_file: 'తొలగించు',
            ocr_result: 'OCR ఫలితం',
            waiting_for_file: 'ఫైల్ కోసం వేచి ఉంది',
            no_prescription_scanned: 'ఇంకా ఏ ప్రిస్క్రిప్షన్ కూడా స్కాన్ కాలేదు.',
            confirm_extracted_details: 'ఎక్స్ట్రాక్ట్ చేయబడిన వివరాలను నిర్ధారించండి',
            confirm_and_save: 'నిర్ధారించి సేవ్ చేయండి',
            medication_safety: 'మందు భద్రత',
            safety_check: 'సేఫ్టీ చెక్',
            safety_review: 'సేఫ్టీ రివ్యూ',
            no_safety_alerts: 'సేఫ్టీ అల్లర్ట్లు లేవు.',
            urgent_help: 'అత్యవసర సహాయం',
            emergency_info_title: 'అత్యవసర మరియు సేఫ్టీ సమాచారం',
            emergency_warning: 'మీకు తీవ్రమైన మరియు జీవితానికి హాని కలిగించే ప్రతిచర్య ఉన్నట్లయితే వెంటనే వృత్తిపరమైన/అత్యవసర వైద్య సహాయం తీసుకోండి.',
            emergency_note: 'అర్హత గల ఆరోగ్యరక్షణ నిపుణుడితో మాట్లాడకుండానే సొంత నిర్ధారణ లేదా మందు మార్పులు చేయవద్దు.',
            emergency_list_breathing: 'శ్వాసలో ఇబ్బంది',
            emergency_list_swelling: 'తీవ్రమైన వాపు',
            emergency_list_unconscious: 'మతిమరుపు',
            emergency_list_chest_pain: 'తీవ్రమైన ఛాతీ నొప్పి',
            emergency_list_confusion: 'తీవ్రమైన గందరగోళం',
            emergency_list_allergy: 'తీవ్రమైన అలెర్జీ ప్రతిచర్య లక్షణాలు',
        },
        hi: {
            brand_title_short: 'स्मार्टमेड',
            brand_title_suffix: 'कम्पैनियन',
            brand_title: 'स्मार्टमेड',
            brand_subtitle: 'मल्टीमोडल प्रिस्क्रिप्शन & मेडिकेशन सुरक्षा सहायक',
            dashboard: 'डैशबोर्ड',
            prescriptions: 'प्रिस्क्रिप्शन स्कैनर',
            medicines: 'दवाइयाँ',
            reminders: 'रिमाइंडर',
            safety: 'सुरक्षा',
            emergency: 'आपातकाल',
            settings: 'सेटिंग्स',
            search: 'खोजें',
            notifications: 'सूचनाएँ',
            profile_title: 'आपकी प्रोफ़ाइल',
            full_name_field: 'पूरा नाम',
            username_field: 'उपयोगकर्ता नाम',
            save_profile_button: 'प्रोफ़ाइल सेव करें',
            notification_title: 'सूचनाएँ',
            no_notifications: 'कोई नई सूचना नहीं है।',
            view_reminders: 'रिमाइंडर देखें',
            profile: 'प्रोफ़ाइल',
            good_evening: 'शुभ संध्या',
            demo_mode: 'डेमो मोड',
            todays_medicines: 'आज की दवाइयाँ',
            active_prescriptions: '{count} सक्रिय प्रिस्क्रिप्शन्स',
            upcoming_reminders: 'आगामी रिमाइंडर',
            next_scheduled_reminder: 'अगला निर्धारित रिमाइंडर',
            safety_alerts: 'सुरक्षा अलर्ट',
            review_instructions: 'निर्देश देखें',
            recent_prescriptions: 'हाल की प्रिस्क्रिप्शन',
            stored_records: 'सहेजे गए रिकॉर्ड',
            todays_medicines_panel: 'आज की दवाइयाँ',
            active_status: 'सक्रिय',
            edit_button: 'संपादित',
            delete_button: 'हटाएँ',
            upcoming_reminders_panel: 'आगामी रिमाइंडर',
            recent_prescriptions_panel: 'हाल की प्रिस्क्रिप्शन',
            safety_alerts_panel: 'सुरक्षा अलर्ट',
            medication_schedule: 'दवा अनुसूची',
            reminders_page_title: 'रिमाइंडर',
            add_reminder_button: 'रिमाइंडर जोड़ें',
            medicine_name_field: 'दवा का नाम',
            time_field: 'समय',
            frequency_field: 'आवृत्ति',
            notes_field: 'नोट्स',
            save_reminder_button: 'रिमाइंडर सेव करें',
            cancel_button: 'रद्द करें',
            save_changes_button: 'परिवर्तन सेव करें',
            no_medicines_added: 'अभी तक कोई दवा नहीं जोड़ी गई है।',
            no_reminders_scheduled: 'कोई रिमाइंडर निर्धारित नहीं है।',
            no_prescriptions_uploaded: 'अभी तक कोई प्रिस्क्रिप्शन अपलोड नहीं किया गया है।',
            no_safety_warnings: 'इस समय कोई सुरक्षा चेतावनी नहीं है।',
            table_name: 'नाम',
            created_date: 'तारीख बनाई गई',
            actions: 'कार्य',
            no_medicines_yet: 'अभी तक कोई दवा नहीं है। प्रिस्क्रिप्शन या मैनुअल एंट्री से जोड़ें।',
            medication_list: 'दवाइयों की सूची',
            medicines_page_title: 'दवाइयाँ',
            add_medicine_button: 'दवा जोड़ें',
            strength_field: 'शक्ति',
            duration_field: 'अवधि',
            instructions_field: 'निर्देश',
            source_field: 'स्रोत',
            save_medicine_button: 'दवा सेव करें',
            disclaimer: 'SmartMed Companion एक शैक्षिक और दवा-सहायक उपकरण है। यह डॉक्टर या फार्मासिस्ट की सलाह, निदान या उपचार का विकल्प नहीं है।',
            prescription_intake: 'प्रिस्क्रिप्शन इन्टेक',
            prescription_scanner_title: 'प्रिस्क्रिप्शन स्कैनर',
            upload_prescription: 'प्रिस्क्रिप्शन इमेज या PDF अपलोड करें',
            drag_drop_instruction: 'फ़ाइल को ड्रैग करें या अपने डिवाइस से चुनें।',
            choose_file: 'फ़ाइल चुनें',
            scan_extract: 'स्कैन और एक्सट्रैक्ट',
            remove_file: 'हटाएँ',
            ocr_result: 'OCR परिणाम',
            waiting_for_file: 'फ़ाइल का इंतज़ार',
            no_prescription_scanned: 'अभी तक कोई प्रिस्क्रिप्शन स्कैन नहीं हुआ है।',
            confirm_extracted_details: 'निकाले गए विवरण की पुष्टि करें',
            confirm_and_save: 'पुष्टि करें और सेव करें',
            medication_safety: 'दवा सुरक्षा',
            safety_check: 'सुरक्षा जांच',
            safety_review: 'सुरक्षा समीक्षा',
            no_safety_alerts: 'कोई सुरक्षा अलर्ट नहीं मिला।',
            urgent_help: 'तत्काल सहायता',
            emergency_info_title: 'आपातकाल और सुरक्षा जानकारी',
            emergency_warning: 'यदि आप गंभीर या जीवन-घातक प्रतिक्रिया का अनुभव कर रहे हैं, तो तुरंत पेशेवर/आपातकालीन चिकित्सा सहायता लें।',
            emergency_note: 'किसी योग्य स्वास्थ्य देखभाल पेशेवर से बात किए बिना आत्म-निदान या दवा बदलाव न करें।',
            emergency_list_breathing: 'साँस लेने में कठिनाई',
            emergency_list_swelling: 'गंभीर सूजन',
            emergency_list_unconscious: 'बेहोशी',
            emergency_list_chest_pain: 'गंभीर छाती दर्द',
            emergency_list_confusion: 'गंभीर भ्रम',
            emergency_list_allergy: 'गंभीर एलर्जी प्रतिक्रिया के लक्षण',
        }
    };

    const applyLanguage = (language) => {
        const lang = translations[language] ? language : 'en';
        document.documentElement.lang = lang;
        const select = document.getElementById('language-select');
        if (select) {
            select.value = lang;
        }

        document.querySelectorAll('[data-i18n]').forEach((element) => {
            const key = element.dataset.i18n;
            const template = translations[lang][key] || key;
            const count = element.dataset.count;
            let label = template;
            if (count !== undefined && template.includes('{count}')) {
                label = template.replace('{count}', count);
            }
            const emoji = element.dataset.emoji || '';
            element.textContent = `${emoji}${label}`;
        });

        const searchInput = document.getElementById('global-search-input');
        if (searchInput) {
            searchInput.placeholder = translations[lang].search || 'Search';
        }

        localStorage.setItem('smartmed_lang', lang);
    };

    const storedLanguage = localStorage.getItem('smartmed_lang') || 'en';
    applyLanguage(storedLanguage);

    const languageSelect = document.getElementById('language-select');
    languageSelect?.addEventListener('change', (event) => {
        applyLanguage(event.target.value);
    });

    const globalSearchForm = document.getElementById('global-search-form');
    const globalSearchInput = document.getElementById('global-search-input');
    const params = new URLSearchParams(window.location.search);
    if (globalSearchInput && params.get('q')) {
        globalSearchInput.value = params.get('q');
    }
    globalSearchForm?.addEventListener('submit', (event) => {
        if (!globalSearchInput || !globalSearchInput.value.trim()) {
            event.preventDefault();
            window.location.href = '/medicines';
        }
    });

    // Toggle the category menu on mobile
    const mobileMenuBtn = document.querySelector('.mobile-menu-btn');
    const menuDropdown = document.querySelector('.menu-dropdown');
    const dropdownItems = document.querySelectorAll('.dropdown-item');
    const notificationMenu = document.querySelector('.notification-menu');
    const notificationButton = notificationMenu?.querySelector('.action-button');
    const profileMenu = document.querySelector('.profile-menu');
    const profileButton = profileMenu?.querySelector('.profile-pill');
    const profileFullName = document.getElementById('profile-full-name');
    const profileUsername = document.getElementById('profile-username');
    const saveProfileButton = document.getElementById('save-profile');

    const updateProfileDisplay = (fullName, username) => {
        const name = fullName || 'Alex Johnson';
        const initials = name.split(/\s+/).filter(Boolean).map(part => part[0]).join('').slice(0, 2).toUpperCase();
        document.querySelectorAll('.profile-pill, .profile-avatar-large').forEach(element => {
            element.textContent = initials || 'AJ';
        });
        const welcomeName = document.getElementById('welcome-name');
        if (welcomeName) {
            welcomeName.textContent = name;
        }
        if (profileFullName) profileFullName.value = name;
        if (profileUsername) profileUsername.value = username || 'alex';
    };

    const savedProfile = JSON.parse(localStorage.getItem('smartmed_profile') || 'null');
    updateProfileDisplay(savedProfile?.fullName, savedProfile?.username);

    if (mobileMenuBtn) {
        mobileMenuBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            menuDropdown?.classList.toggle('open');
            mobileMenuBtn.setAttribute(
                'aria-expanded',
                menuDropdown?.classList.contains('open') ? 'true' : 'false'
            );
        });
    }

    // Close dropdown when clicking a dropdown item
    dropdownItems.forEach(item => {
        item.addEventListener('click', () => {
            menuDropdown?.classList.remove('open');
            mobileMenuBtn?.setAttribute('aria-expanded', 'false');
        });
    });

    notificationButton?.addEventListener('click', (event) => {
        event.stopPropagation();
        notificationMenu.classList.toggle('open');
        notificationButton.setAttribute(
            'aria-expanded',
            notificationMenu.classList.contains('open') ? 'true' : 'false'
        );
    });

    profileButton?.addEventListener('click', (event) => {
        event.stopPropagation();
        profileMenu.classList.toggle('open');
        profileButton.setAttribute('aria-expanded', profileMenu.classList.contains('open') ? 'true' : 'false');
    });

    saveProfileButton?.addEventListener('click', () => {
        const fullName = profileFullName?.value.trim();
        const username = profileUsername?.value.trim();
        if (!fullName || !username) {
            window.showToast('Please enter your full name and username.', 'warning');
            return;
        }
        localStorage.setItem('smartmed_profile', JSON.stringify({ fullName, username }));
        updateProfileDisplay(fullName, username);
        profileMenu?.classList.remove('open');
        profileButton?.setAttribute('aria-expanded', 'false');
        window.showToast('Profile saved successfully.', 'success');
    });

    // Close dropdown when clicking outside
    document.addEventListener('click', (e) => {
        if (!menuDropdown?.contains(e.target) && e.target !== mobileMenuBtn) {
            menuDropdown?.classList.remove('open');
            mobileMenuBtn?.setAttribute('aria-expanded', 'false');
        }
        if (!notificationMenu?.contains(e.target)) {
            notificationMenu?.classList.remove('open');
            notificationButton?.setAttribute('aria-expanded', 'false');
        }
        if (!profileMenu?.contains(e.target)) {
            profileMenu?.classList.remove('open');
            profileButton?.setAttribute('aria-expanded', 'false');
        }
    });

    const medicineForm = document.getElementById('medicine-form');
    if (medicineForm) {
        medicineForm.addEventListener('submit', async (event) => {
            event.preventDefault();

            const formData = new FormData(medicineForm);
            const payload = Object.fromEntries(
                Array.from(formData.entries()).map(([key, value]) => [key, String(value).trim()])
            );

            if (!payload.name) {
                window.showToast('Please enter a medicine name.', 'warning');
                return;
            }

            try {
                const response = await fetch('/medicines', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        ...payload,
                        source: payload.source || 'User-entered'
                    })
                });

                const result = await response.json().catch(() => ({}));
                if (!response.ok) {
                    throw new Error(result.detail || 'Unable to add medicine.');
                }

                window.showToast('Medicine added successfully.', 'success');
                medicineForm.reset();
                const panel = document.getElementById('medicine-form-panel');
                if (panel && window.bootstrap) {
                    const collapse = window.bootstrap.Collapse.getInstance(panel) || new window.bootstrap.Collapse(panel, { toggle: false });
                    collapse.hide();
                }
                setTimeout(() => window.location.reload(), 400);
            } catch (error) {
                window.showToast(error.message || 'Unable to add medicine.', 'error');
            }
        });
    }

    const dashboardForm = document.getElementById('dashboard-medicine-form');
    const cancelButton = document.getElementById('cancel-medicine-edit');

    const hideDashboardMedicineForm = () => {
        if (dashboardForm) {
            dashboardForm.classList.add('hidden');
            dashboardForm.reset();
        }
    };

    const collectMedicineFormData = () => {
        const id = document.getElementById('dashboard-medicine-id')?.value;
        const formData = new FormData(dashboardForm);
        const payload = Object.fromEntries(
            Array.from(formData.entries()).map(([key, value]) => [key, String(value).trim()])
        );
        return { id, payload };
    };

    cancelButton?.addEventListener('click', hideDashboardMedicineForm);

    document.querySelectorAll('[data-medicine-action]').forEach((button) => {
        button.addEventListener('click', async () => {
            const action = button.dataset.medicineAction;
            const medicineId = button.dataset.medicineId;

            if (action === 'delete') {
                const confirmed = window.confirm('Delete this medicine record?');
                if (!confirmed) return;

                try {
                    const response = await fetch(`/medicines/${medicineId}`, { method: 'DELETE' });
                    const result = await response.json().catch(() => ({}));
                    if (!response.ok) throw new Error(result.detail || 'Unable to delete medicine.');
                    window.showToast('Medicine deleted.', 'success');
                    setTimeout(() => window.location.reload(), 350);
                } catch (error) {
                    window.showToast(error.message || 'Unable to delete medicine.', 'error');
                }
                return;
            }

            if (action === 'edit' && dashboardForm) {
                const values = {
                    name: button.dataset.name || '',
                    strength: button.dataset.strength || '',
                    frequency: button.dataset.frequency || '',
                    duration: button.dataset.duration || '',
                    instructions: button.dataset.instructions || '',
                    source: button.dataset.source || 'User-entered'
                };

                document.getElementById('dashboard-medicine-id').value = medicineId;
                document.getElementById('dashboard-medicine-name').value = values.name;
                document.getElementById('dashboard-medicine-strength').value = values.strength;
                document.getElementById('dashboard-medicine-frequency').value = values.frequency;
                document.getElementById('dashboard-medicine-duration').value = values.duration;
                document.getElementById('dashboard-medicine-instructions').value = values.instructions;
                document.getElementById('dashboard-medicine-source').value = values.source;
                dashboardForm.classList.remove('hidden');
                document.getElementById('dashboard-medicine-name').focus();
            }
        });
    });

    dashboardForm?.addEventListener('submit', async (event) => {
        event.preventDefault();
        const { id, payload } = collectMedicineFormData();

        if (!id || !payload.name) {
            window.showToast('Please enter a medicine name.', 'warning');
            return;
        }

        try {
            const response = await fetch(`/medicines/${id}`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });
            const result = await response.json().catch(() => ({}));
            if (!response.ok) throw new Error(result.detail || 'Unable to update medicine.');
            window.showToast('Medicine updated successfully.', 'success');
            hideDashboardMedicineForm();
            setTimeout(() => window.location.reload(), 350);
        } catch (error) {
            window.showToast(error.message || 'Unable to update medicine.', 'error');
        }
    });
});

from __future__ import annotations

from .models import Diagnosis, KnowledgeBase, Question, Rule, SymptomPath


def build_knowledge_base() -> KnowledgeBase:
    questions = {
        "is_laptop": Question(
            fact="is_laptop",
            prompt="Is the affected computer a laptop?",
            help_text="Select Yes for a laptop and No for a desktop tower or all-in-one PC.",
        ),
        "no_power_signs": Question(
            fact="no_power_signs",
            prompt="When you press the power button, are there no lights, fan movement, or startup sounds?",
            help_text="If the machine looks completely dead, answer Yes.",
        ),
        "same_outlet_fails_other_device": Question(
            fact="same_outlet_fails_other_device",
            prompt="Do other devices also fail when plugged into the same wall outlet?",
            help_text="You can test a phone charger, lamp, or another low-risk device.",
        ),
        "battery_not_charging": Question(
            fact="battery_not_charging",
            prompt="Is the battery icon or charging light showing that the laptop is not charging?",
            help_text="If the battery level never rises while plugged in, answer Yes.",
        ),
        "charger_or_cable_damaged": Question(
            fact="charger_or_cable_damaged",
            prompt="Is the charger, power brick, or cable visibly damaged, loose, or overheating?",
            help_text="Do not keep using a charger that is frayed, burnt, or very hot.",
        ),
        "power_source_verified": Question(
            fact="power_source_verified",
            prompt="Have you already tried another known-good outlet or power source with the same result?",
            help_text="This helps separate an internal fault from an external power issue.",
        ),
        "power_cable_secure": Question(
            fact="power_cable_secure",
            prompt="Is the power cable firmly connected on both ends?",
            help_text="Check both the computer side and the wall or power brick side.",
        ),
        "no_boot_device_message": Question(
            fact="no_boot_device_message",
            prompt="Do you see a message such as 'No boot device', 'Operating system not found', or similar?",
            help_text="Messages about missing operating systems usually point to storage or boot order problems.",
        ),
        "repeated_beeps": Question(
            fact="repeated_beeps",
            prompt="Do you hear repeated beep sounds during startup?",
            help_text="Beep patterns often indicate a RAM or POST hardware fault.",
        ),
        "blank_screen_after_power_on": Question(
            fact="blank_screen_after_power_on",
            prompt="After powering on, does the screen stay blank even though the lights or fan start?",
            help_text="Answer Yes if the machine powers up but never reaches a normal login or desktop screen.",
        ),
        "disk_clicking_noise": Question(
            fact="disk_clicking_noise",
            prompt="Do you hear clicking, grinding, or repeated spin-up noises from the storage drive?",
            help_text="Mechanical clicking from an HDD is a strong warning sign of drive failure.",
        ),
        "boot_loops_after_logo": Question(
            fact="boot_loops_after_logo",
            prompt="Does the PC restart repeatedly after showing the manufacturer logo or loading screen?",
            help_text="If it never reaches the desktop and keeps restarting, answer Yes.",
        ),
        "screen_is_black": Question(
            fact="screen_is_black",
            prompt="Is the screen black even though the computer seems to be running?",
            help_text="For example, you hear startup sounds or see keyboard lights but the display stays dark.",
        ),
        "screen_is_dim": Question(
            fact="screen_is_dim",
            prompt="Is the screen extremely dim, as if the backlight is off?",
            help_text="Try raising the brightness first; if it remains barely visible, answer Yes.",
        ),
        "external_monitor_works": Question(
            fact="external_monitor_works",
            prompt="When you connect an external monitor or TV, does it display normally?",
            help_text="If the external display works, the internal screen or cable is more likely at fault.",
        ),
        "screen_flickers": Question(
            fact="screen_flickers",
            prompt="Does the screen flicker, flash, or show unstable graphics?",
            help_text="Answer Yes for repeated flicker, flashing, or sudden visual distortion.",
        ),
        "graphics_artifacts": Question(
            fact="graphics_artifacts",
            prompt="Do you see lines, colored blocks, or visual artifacts on the screen?",
            help_text="Artifacts usually suggest a graphics processing or display hardware problem.",
        ),
        "device_gets_hot": Question(
            fact="device_gets_hot",
            prompt="Does the computer become very hot during normal use?",
            help_text="Use touch carefully; if the case becomes unusually hot, answer Yes.",
        ),
        "fan_is_loud": Question(
            fact="fan_is_loud",
            prompt="Does the cooling fan run loudly for long periods?",
            help_text="Constant loud fan noise often means restricted airflow or heavy heat load.",
        ),
        "vent_blocked_or_dusty": Question(
            fact="vent_blocked_or_dusty",
            prompt="Are the air vents blocked, dusty, or used on soft surfaces like a bed or sofa?",
            help_text="Poor airflow is one of the most common overheating causes for home users.",
        ),
        "fan_not_spinning": Question(
            fact="fan_not_spinning",
            prompt="Do you suspect the fan is not spinning or that there is no airflow at all?",
            help_text="If the machine overheats but you hear no fan and feel no airflow, answer Yes.",
        ),
        "single_peripheral_fails": Question(
            fact="single_peripheral_fails",
            prompt="Is only one device such as a mouse, keyboard, printer, or webcam failing?",
            help_text="If the rest of the computer works normally and only one accessory fails, answer Yes.",
        ),
        "device_works_on_other_port": Question(
            fact="device_works_on_other_port",
            prompt="Does the device work when moved to a different port on the same computer?",
            help_text="A working device on another port usually points to a bad port rather than a bad device.",
        ),
        "device_fails_on_other_computer": Question(
            fact="device_fails_on_other_computer",
            prompt="Does the same device also fail on another computer?",
            help_text="If it fails everywhere, the device itself is likely faulty.",
        ),
        "driver_warning_present": Question(
            fact="driver_warning_present",
            prompt="Do you see a warning icon or error for that device in system settings or device manager?",
            help_text="A warning or missing driver message points to a software driver issue.",
        ),
        "slow_startup": Question(
            fact="slow_startup",
            prompt="Does the computer take much longer than usual to start?",
            help_text="Slow startup usually means too many startup tasks, disk pressure, or malware.",
        ),
        "many_startup_apps": Question(
            fact="many_startup_apps",
            prompt="Do many applications open automatically when the computer starts?",
            help_text="Chat tools, launchers, and sync apps commonly slow down startup.",
        ),
        "disk_almost_full": Question(
            fact="disk_almost_full",
            prompt="Is the main storage drive nearly full?",
            help_text="If free space is very low, the system can become slow and unstable.",
        ),
        "unexpected_popups": Question(
            fact="unexpected_popups",
            prompt="Are you seeing unexpected pop-ups, intrusive ads, or security warnings?",
            help_text="Frequent ads or fake warnings often suggest adware or malware.",
        ),
        "browser_redirects": Question(
            fact="browser_redirects",
            prompt="Does your browser redirect you to pages you did not request?",
            help_text="Redirects are a common sign of browser hijacking or adware.",
        ),
        "unknown_programs_installed": Question(
            fact="unknown_programs_installed",
            prompt="Have unknown programs, toolbars, or extensions appeared recently?",
            help_text="Software appearing without your consent is a strong malware signal.",
        ),
        "suspicious_background_activity": Question(
            fact="suspicious_background_activity",
            prompt="Do you notice unusual CPU, disk, or network activity when the computer is idle?",
            help_text="If the machine stays busy while you are doing nothing, answer Yes.",
        ),
        "multiple_devices_offline": Question(
            fact="multiple_devices_offline",
            prompt="Are other phones or computers on the same network also offline?",
            help_text="If everything on the network is down, the router or ISP is more likely responsible.",
        ),
        "wifi_connected_but_no_internet": Question(
            fact="wifi_connected_but_no_internet",
            prompt="Does the computer show that it is connected to Wi-Fi but internet pages still fail to load?",
            help_text="Answer Yes if the Wi-Fi icon says connected but browsing still fails.",
        ),
        "wifi_option_missing": Question(
            fact="wifi_option_missing",
            prompt="Is the Wi-Fi option missing or is the wireless adapter not listed?",
            help_text="Missing Wi-Fi controls often means the adapter is disabled or the driver is broken.",
        ),
        "airplane_mode_off": Question(
            fact="airplane_mode_off",
            prompt="Is airplane mode definitely turned off?",
            help_text="If you are sure airplane mode is off, answer Yes.",
        ),
        "browser_dns_errors": Question(
            fact="browser_dns_errors",
            prompt="Do you see DNS or 'server not found' style errors in the browser?",
            help_text="DNS failures often point to a local configuration problem.",
        ),
        "single_app_problem": Question(
            fact="single_app_problem",
            prompt="Is the issue limited to one application while the rest of the system works?",
            help_text="If only one app is affected, answer Yes.",
        ),
        "app_crashes_after_update": Question(
            fact="app_crashes_after_update",
            prompt="Did the application start failing right after an update or reinstall?",
            help_text="A fresh crash right after an update often means a corrupted install or bad patch.",
        ),
        "compatibility_message": Question(
            fact="compatibility_message",
            prompt="Does the error message mention compatibility, version, or unsupported operating system?",
            help_text="This usually means the software version does not match the system.",
        ),
        "install_requires_permissions": Question(
            fact="install_requires_permissions",
            prompt="Does installation fail because of permissions or administrator access?",
            help_text="Permission-related failures usually need an administrator-approved install.",
        ),
        "antivirus_disabled": Question(
            fact="antivirus_disabled",
            prompt="Is antivirus or real-time protection turned off without you doing it?",
            help_text="Unexpectedly disabled security tools are suspicious and should be checked quickly.",
        ),
        "problem_started_after_system_update": Question(
            fact="problem_started_after_system_update",
            prompt="Did the issue begin immediately after a system update?",
            help_text="A clear change after an update often points to a bad patch or driver conflict.",
        ),
        "can_reach_safe_mode": Question(
            fact="can_reach_safe_mode",
            prompt="Can the computer start in safe mode or recovery mode?",
            help_text="If safe mode works but normal startup does not, the problem is often software-related.",
        ),
        "blue_screen_or_stop_error": Question(
            fact="blue_screen_or_stop_error",
            prompt="Do you get a blue screen or stop error during startup or use?",
            help_text="A stop error after an update often indicates a system or driver conflict.",
        ),
        "login_problem": Question(
            fact="login_problem",
            prompt="Is the main problem that you cannot sign in to your account?",
            help_text="If the system boots but you cannot access your user account, answer Yes.",
        ),
        "freezes_under_light_use": Question(
            fact="freezes_under_light_use",
            prompt="Does the computer freeze or lag even during light tasks like browsing or typing?",
            help_text="If the system struggles during simple tasks, answer Yes.",
        ),
    }

    rules = (
        Rule(
            id="power_outlet",
            conclusion="wall_outlet_problem",
            premises=("no_power_signs", "same_outlet_fails_other_device"),
            explanation="The computer shows no power and the wall outlet is also failing for other devices.",
        ),
        Rule(
            id="charger_battery",
            conclusion="charger_or_battery_problem",
            premises=("is_laptop", "no_power_signs", "battery_not_charging", "charger_or_cable_damaged"),
            explanation="The laptop has no power response, it is not charging, and the charger or cable looks faulty.",
        ),
        Rule(
            id="internal_power",
            conclusion="internal_power_issue",
            premises=("no_power_signs", "power_source_verified", "power_cable_secure"),
            explanation="External power has already been verified, so the remaining cause is likely inside the computer.",
        ),
        Rule(
            id="boot_device",
            conclusion="boot_device_problem",
            premises=("no_boot_device_message",),
            explanation="The boot error message directly points to a storage detection or boot order issue.",
        ),
        Rule(
            id="ram_post",
            conclusion="ram_or_post_issue",
            premises=("repeated_beeps", "blank_screen_after_power_on"),
            explanation="Repeated beeps with a blank screen strongly suggest a POST or memory problem.",
        ),
        Rule(
            id="storage_failure",
            conclusion="storage_hardware_failure",
            premises=("disk_clicking_noise", "boot_loops_after_logo"),
            explanation="Disk noises together with repeated failed boots indicate probable drive failure.",
        ),
        Rule(
            id="internal_display",
            conclusion="internal_display_problem",
            premises=("screen_is_black", "external_monitor_works"),
            explanation="The computer runs and an external display works, so the internal display path is the likely issue.",
        ),
        Rule(
            id="graphics_hw",
            conclusion="graphics_problem",
            premises=("screen_flickers", "graphics_artifacts"),
            explanation="Flicker plus visible artifacts usually indicate a graphics or display hardware fault.",
        ),
        Rule(
            id="airflow_heat",
            conclusion="overheating_due_to_airflow",
            premises=("device_gets_hot", "fan_is_loud", "vent_blocked_or_dusty"),
            explanation="The device is hot, the fan is overworking, and airflow is restricted.",
        ),
        Rule(
            id="fan_failure",
            conclusion="fan_failure_problem",
            premises=("device_gets_hot", "fan_not_spinning"),
            explanation="Severe heat without normal fan airflow suggests a cooling fan fault.",
        ),
        Rule(
            id="bad_port",
            conclusion="physical_port_problem",
            premises=("single_peripheral_fails", "device_works_on_other_port"),
            explanation="The device works elsewhere on the same computer, so the original port is the likely fault.",
        ),
        Rule(
            id="device_driver",
            conclusion="device_driver_problem",
            premises=("single_peripheral_fails", "driver_warning_present"),
            explanation="The peripheral issue is limited to one device and the system reports a driver warning.",
        ),
        Rule(
            id="bad_peripheral",
            conclusion="peripheral_hardware_problem",
            premises=("single_peripheral_fails", "device_fails_on_other_computer"),
            explanation="The accessory fails on multiple machines, which points to a hardware fault in the device itself.",
        ),
        Rule(
            id="low_storage",
            conclusion="low_storage_problem",
            premises=("freezes_under_light_use", "disk_almost_full"),
            explanation="The computer is freezing under light load and the storage is nearly full.",
        ),
        Rule(
            id="startup_overload",
            conclusion="startup_overload",
            premises=("slow_startup", "many_startup_apps"),
            explanation="Slow startup combined with many launch-at-login apps points to startup overload.",
        ),
        Rule(
            id="malware_redirects",
            conclusion="malware_problem",
            premises=("unexpected_popups", "browser_redirects"),
            explanation="Pop-ups plus browser redirects strongly suggest adware or malware.",
        ),
        Rule(
            id="malware_unknown_apps",
            conclusion="malware_problem",
            premises=("unexpected_popups", "unknown_programs_installed"),
            explanation="Unexpected software appearing alongside pop-ups strongly suggests malware.",
        ),
        Rule(
            id="malware_security_disabled",
            conclusion="malware_problem",
            premises=("suspicious_background_activity", "antivirus_disabled"),
            explanation="Suspicious background activity together with disabled protection is a common malware pattern.",
        ),
        Rule(
            id="router_or_isp",
            conclusion="router_or_isp_problem",
            premises=("multiple_devices_offline",),
            explanation="If several devices are offline at the same time, the wider network is the likely issue.",
        ),
        Rule(
            id="network_adapter",
            conclusion="network_adapter_problem",
            premises=("wifi_option_missing", "airplane_mode_off"),
            explanation="The wireless controls are missing even though airplane mode is off, which suggests an adapter or driver issue.",
        ),
        Rule(
            id="local_network_config",
            conclusion="local_network_configuration_problem",
            premises=("wifi_connected_but_no_internet", "browser_dns_errors"),
            explanation="The computer is connected to Wi-Fi but failing on DNS or name resolution.",
        ),
        Rule(
            id="app_permissions",
            conclusion="permission_issue",
            premises=("install_requires_permissions",),
            explanation="The installation is being blocked by missing permission or administrator rights.",
        ),
        Rule(
            id="app_compatibility",
            conclusion="application_compatibility_problem",
            premises=("single_app_problem", "compatibility_message"),
            explanation="The issue is isolated to one app and the error message indicates a version mismatch.",
        ),
        Rule(
            id="app_corruption",
            conclusion="application_corruption_problem",
            premises=("single_app_problem", "app_crashes_after_update"),
            explanation="The application began failing right after an update or reinstall, which suggests a corrupted installation.",
        ),
        Rule(
            id="security_config",
            conclusion="antivirus_configuration_problem",
            premises=("antivirus_disabled",),
            explanation="Security protection is disabled and needs immediate verification or re-enablement.",
        ),
        Rule(
            id="update_conflict",
            conclusion="update_or_driver_conflict",
            premises=("problem_started_after_system_update", "blue_screen_or_stop_error"),
            explanation="A stop error that began right after an update usually indicates an update or driver conflict.",
        ),
        Rule(
            id="login_profile",
            conclusion="login_configuration_problem",
            premises=("login_problem", "can_reach_safe_mode"),
            explanation="If login fails but safe mode is still reachable, the issue is likely in the user profile or startup configuration.",
        ),
    )

    diagnoses = {
        "wall_outlet_problem": Diagnosis(
            id="wall_outlet_problem",
            title="External power outlet problem",
            category="hardware",
            summary="The computer is probably not receiving power from the wall outlet or power strip.",
            recommendations=(
                "Try a different known-good wall outlet without using a damaged extension or power strip.",
                "Test the current outlet with another simple device such as a lamp or phone charger.",
                "If using a surge protector, reset it or bypass it temporarily with a safe direct connection.",
            ),
            escalation=(
                "Escalate if you notice sparks, burning smell, or signs of electrical damage.",
                "Escalate if the outlet still appears faulty after safe external checks.",
            ),
        ),
        "charger_or_battery_problem": Diagnosis(
            id="charger_or_battery_problem",
            title="Laptop charger or battery problem",
            category="hardware",
            summary="The laptop is likely failing to power on because the charger, charging cable, or battery is defective.",
            recommendations=(
                "Inspect the charger and cable for cuts, bent connectors, or overheating, and stop using damaged parts.",
                "Try a known-good compatible charger if one is available.",
                "If the battery is removable and safe to access, test power with the charger only.",
            ),
            escalation=(
                "Escalate if the charger becomes very hot, smells burnt, or the charging port is loose.",
                "Escalate if a known-good charger still gives no charging response.",
            ),
        ),
        "internal_power_issue": Diagnosis(
            id="internal_power_issue",
            title="Possible internal power hardware failure",
            category="hardware",
            summary="External power has been checked, so the fault is likely in the power supply, motherboard, or internal power circuit.",
            recommendations=(
                "Disconnect the machine from power for a few minutes, then reconnect and try again.",
                "Remove non-essential external devices before another power attempt.",
                "Do not open the power supply or motherboard area if you are not trained.",
            ),
            escalation=(
                "Escalate to a technician for internal hardware inspection.",
                "Escalate immediately if there was a recent power surge or you smell burning components.",
            ),
        ),
        "boot_device_problem": Diagnosis(
            id="boot_device_problem",
            title="Boot device or storage detection problem",
            category="hardware",
            summary="The system cannot find the operating system on the expected drive.",
            recommendations=(
                "Restart once and check whether external USB devices are connected that could confuse the boot order.",
                "If you know how, verify in BIOS or UEFI that the main storage drive is detected.",
                "Run the operating system recovery or startup repair tools if they are available.",
            ),
            escalation=(
                "Escalate if the main drive is missing from BIOS or UEFI.",
                "Escalate if startup repair cannot detect the operating system.",
            ),
        ),
        "ram_or_post_issue": Diagnosis(
            id="ram_or_post_issue",
            title="RAM or POST hardware problem",
            category="hardware",
            summary="The computer is likely failing its power-on self-test, commonly because of memory or another internal component.",
            recommendations=(
                "Power the machine off completely and disconnect all non-essential accessories.",
                "If the computer was moved recently, check for any obvious loose external connections.",
                "Avoid repeatedly forcing startup if the same beep pattern continues.",
            ),
            escalation=(
                "Escalate for internal RAM or motherboard inspection.",
                "Escalate immediately if the machine emits a repeated beep code on every attempt.",
            ),
        ),
        "storage_hardware_failure": Diagnosis(
            id="storage_hardware_failure",
            title="Possible storage drive failure",
            category="hardware",
            summary="The system is showing classic signs of a failing hard drive or storage device.",
            recommendations=(
                "Stop unnecessary restarts and heavy use to reduce the risk of further data loss.",
                "If the computer still starts occasionally, back up important files immediately.",
                "Use disk health or recovery tools only if the system remains accessible.",
            ),
            escalation=(
                "Escalate if the drive keeps clicking or the system cannot detect it anymore.",
                "Escalate quickly if important data must be recovered.",
            ),
        ),
        "internal_display_problem": Diagnosis(
            id="internal_display_problem",
            title="Internal display or display cable problem",
            category="hardware",
            summary="The computer appears to work, but the built-in screen or its connection path is likely faulty.",
            recommendations=(
                "Use an external monitor temporarily if one is available.",
                "Raise brightness fully and restart once to rule out a simple brightness issue.",
                "If this is a laptop, avoid twisting the screen or forcing the hinge area.",
            ),
            escalation=(
                "Escalate if the internal display stays black while an external monitor works normally.",
                "Escalate if opening or moving the lid changes the display behavior.",
            ),
        ),
        "graphics_problem": Diagnosis(
            id="graphics_problem",
            title="Graphics hardware problem",
            category="hardware",
            summary="The flicker and visual artifacts suggest a GPU or graphics path hardware issue.",
            recommendations=(
                "Restart the computer and reduce demanding graphics tasks for now.",
                "If possible, update the graphics driver once before assuming permanent hardware failure.",
                "Check whether the issue also appears on an external display.",
            ),
            escalation=(
                "Escalate if artifacts appear before login or during BIOS startup.",
                "Escalate if driver updates do not change the behavior.",
            ),
        ),
        "overheating_due_to_airflow": Diagnosis(
            id="overheating_due_to_airflow",
            title="Overheating caused by restricted airflow",
            category="hardware",
            summary="The cooling system is working hard, but airflow is blocked or insufficient.",
            recommendations=(
                "Move the computer to a hard flat surface with clear vent space.",
                "Clean outer vents carefully with the machine powered off.",
                "Close heavy applications and let the system cool down before extended use.",
            ),
            escalation=(
                "Escalate if shutdowns continue after airflow is improved.",
                "Escalate if the vents are clear but temperatures remain extreme.",
            ),
        ),
        "fan_failure_problem": Diagnosis(
            id="fan_failure_problem",
            title="Cooling fan failure",
            category="hardware",
            summary="The system is overheating because the cooling fan may not be operating correctly.",
            recommendations=(
                "Power the system down and avoid long use until cooling is restored.",
                "Check for blocked vents from the outside only; do not force the fan manually.",
                "Use the computer for backup only if absolutely necessary and only for short periods.",
            ),
            escalation=(
                "Escalate for internal cleaning or fan replacement.",
                "Escalate immediately if the device shuts down from heat.",
            ),
        ),
        "physical_port_problem": Diagnosis(
            id="physical_port_problem",
            title="Faulty computer port",
            category="hardware",
            summary="The accessory works on another port, so the original port is likely damaged or unstable.",
            recommendations=(
                "Use a different working port if possible.",
                "Inspect the faulty port for bent pins, debris, or looseness without forcing anything inside it.",
                "Avoid repeatedly reconnecting the device to the bad port.",
            ),
            escalation=(
                "Escalate if several ports in the same area stop working.",
                "Escalate if the port feels physically loose or shows visible damage.",
            ),
        ),
        "device_driver_problem": Diagnosis(
            id="device_driver_problem",
            title="Peripheral driver problem",
            category="hardware",
            summary="The accessory issue is most likely caused by a missing, broken, or incompatible driver.",
            recommendations=(
                "Reconnect the device and reinstall or update its driver from the system tools or the manufacturer package.",
                "Restart the computer after the driver change.",
                "Disconnect the device before reinstalling the driver if the OS recommends it.",
            ),
            escalation=(
                "Escalate if the driver warning remains after reinstalling the driver.",
                "Escalate if the device is still not detected at all.",
            ),
        ),
        "peripheral_hardware_problem": Diagnosis(
            id="peripheral_hardware_problem",
            title="Peripheral hardware failure",
            category="hardware",
            summary="The accessory fails on more than one computer, so the device itself is likely defective.",
            recommendations=(
                "Test with another compatible cable or battery if the accessory uses one.",
                "Use a backup device if available.",
                "Check the manufacturer support guidance for that specific accessory.",
            ),
            escalation=(
                "Escalate if the device is still under warranty and the fault is repeatable.",
                "Escalate if the device shows heat, smell, or physical damage.",
            ),
        ),
        "low_storage_problem": Diagnosis(
            id="low_storage_problem",
            title="Low storage space causing performance problems",
            category="software",
            summary="The computer is struggling because the main drive is too full.",
            recommendations=(
                "Delete or move large unnecessary files and empty the recycle bin or trash.",
                "Uninstall applications you no longer use.",
                "Keep enough free space available before running updates or large downloads.",
            ),
            escalation=(
                "Escalate if the drive fills up again very quickly without explanation.",
                "Escalate if file cleanup is impossible because the disk is reporting errors.",
            ),
        ),
        "startup_overload": Diagnosis(
            id="startup_overload",
            title="Too many startup applications",
            category="software",
            summary="Boot time is being slowed down by too many programs launching automatically.",
            recommendations=(
                "Disable non-essential startup apps from the operating system startup settings.",
                "Restart after the change and measure whether startup improves.",
                "Keep only security, touchpad, and other essential system services enabled at startup.",
            ),
            escalation=(
                "Escalate if startup remains extremely slow even after reducing startup apps.",
                "Escalate if heavy startup activity returns immediately after cleanup.",
            ),
        ),
        "malware_problem": Diagnosis(
            id="malware_problem",
            title="Possible malware or adware infection",
            category="software",
            summary="The current symptoms strongly suggest malware, adware, or a browser hijacker.",
            recommendations=(
                "Run a full scan with a trusted antivirus or antimalware tool.",
                "Remove suspicious browser extensions and recently installed unknown software.",
                "Avoid entering passwords or banking details until the system is scanned and cleaned.",
            ),
            escalation=(
                "Escalate if the antivirus cannot start, is repeatedly disabled, or infections keep returning.",
                "Escalate if sensitive accounts may already have been exposed.",
            ),
        ),
        "router_or_isp_problem": Diagnosis(
            id="router_or_isp_problem",
            title="Router or internet provider problem",
            category="software",
            summary="The whole network appears affected, so the issue is likely outside this one computer.",
            recommendations=(
                "Restart the router or modem if that is safe and normal in your home setup.",
                "Check the router lights and any service outage notice from your provider.",
                "Test again after the network equipment finishes restarting.",
            ),
            escalation=(
                "Escalate to your ISP if several devices remain offline after a router restart.",
                "Escalate if the router shows alarm or red fault indicators.",
            ),
        ),
        "network_adapter_problem": Diagnosis(
            id="network_adapter_problem",
            title="Wireless adapter or Wi-Fi driver problem",
            category="software",
            summary="The Wi-Fi controls are missing, which points to a disabled adapter or broken driver.",
            recommendations=(
                "Restart the computer and check whether Wi-Fi returns.",
                "Re-enable the wireless adapter from device settings if it is disabled.",
                "Reinstall or update the Wi-Fi driver if the adapter shows an error.",
            ),
            escalation=(
                "Escalate if the adapter disappears entirely after restart.",
                "Escalate if Wi-Fi remains unavailable even with a fresh driver.",
            ),
        ),
        "local_network_configuration_problem": Diagnosis(
            id="local_network_configuration_problem",
            title="Local network or DNS configuration problem",
            category="software",
            summary="The computer is connected to Wi-Fi, but name resolution or local network settings are failing.",
            recommendations=(
                "Reconnect to the Wi-Fi network and restart the browser.",
                "Renew the network connection or restart the computer.",
                "Reset DNS or network settings using the operating system network troubleshooting tools.",
            ),
            escalation=(
                "Escalate if the issue persists after a restart and network reset.",
                "Escalate if only this computer fails repeatedly on multiple networks.",
            ),
        ),
        "permission_issue": Diagnosis(
            id="permission_issue",
            title="Application installation permission problem",
            category="software",
            summary="The software is failing because the installer lacks the required permissions.",
            recommendations=(
                "Run the installer with administrator approval if that is allowed on the computer.",
                "Close background copies of the same installer or app before trying again.",
                "Install the application into the default location unless the vendor says otherwise.",
            ),
            escalation=(
                "Escalate if you do not have the required administrator credentials.",
                "Escalate if the installer is blocked by organization policy or security rules.",
            ),
        ),
        "application_compatibility_problem": Diagnosis(
            id="application_compatibility_problem",
            title="Application compatibility problem",
            category="software",
            summary="The software version you are trying to run is probably not compatible with the current system.",
            recommendations=(
                "Check the software requirements and install a version that supports your operating system.",
                "Apply pending operating system updates if the application requires a newer platform.",
                "Use the vendor-recommended compatibility mode only if the vendor supports it.",
            ),
            escalation=(
                "Escalate if the application is business-critical and no compatible version is available.",
                "Escalate if the error persists despite using the officially supported version.",
            ),
        ),
        "application_corruption_problem": Diagnosis(
            id="application_corruption_problem",
            title="Corrupted application installation",
            category="software",
            summary="The app likely became unstable because its files were damaged during an update or reinstall.",
            recommendations=(
                "Uninstall the application cleanly and restart before reinstalling it.",
                "Download a fresh installer from the official source only.",
                "Remove leftover cache or temporary files if the vendor documentation recommends it.",
            ),
            escalation=(
                "Escalate if the application still crashes after a clean reinstall.",
                "Escalate if the crash affects multiple user accounts or other apps.",
            ),
        ),
        "antivirus_configuration_problem": Diagnosis(
            id="antivirus_configuration_problem",
            title="Security protection disabled",
            category="software",
            summary="Real-time protection or antivirus has been turned off and needs immediate review.",
            recommendations=(
                "Open the security settings and re-enable real-time protection if it is safe to do so.",
                "Run a full scan as soon as protection is active again.",
                "Remove suspicious recent software that may have disabled security tools.",
            ),
            escalation=(
                "Escalate if the antivirus disables itself again after you turn it on.",
                "Escalate if security settings are locked or cannot be changed.",
            ),
        ),
        "update_or_driver_conflict": Diagnosis(
            id="update_or_driver_conflict",
            title="Recent update or driver conflict",
            category="software",
            summary="The symptoms suggest that a recent update triggered an unstable system or driver state.",
            recommendations=(
                "Use safe mode or recovery mode to remove the recent update if your OS supports it.",
                "Undo the most recent driver change if you know which device was updated.",
                "Create a backup before further repair attempts if the system still starts sometimes.",
            ),
            escalation=(
                "Escalate if blue screens continue in safe mode.",
                "Escalate if the system cannot reach recovery tools.",
            ),
        ),
        "login_configuration_problem": Diagnosis(
            id="login_configuration_problem",
            title="Login or user profile configuration problem",
            category="software",
            summary="The operating system still reaches safe mode, so the problem is likely in the user profile or normal startup configuration.",
            recommendations=(
                "Confirm that the keyboard layout and password entry are correct.",
                "Use safe mode to check for recent startup changes, profile corruption, or pending updates.",
                "Try a password reset or account recovery method supported by the operating system.",
            ),
            escalation=(
                "Escalate if you cannot access any administrative account.",
                "Escalate if the user profile appears corrupted or the login issue affects all accounts.",
            ),
        ),
    }

    symptom_paths = (
        SymptomPath(
            id="hardware_power",
            category="hardware",
            label="Computer does not turn on",
            description="",
            goals=("wall_outlet_problem", "charger_or_battery_problem", "internal_power_issue"),
        ),
        SymptomPath(
            id="hardware_boot",
            category="hardware",
            label="Computer powers on but does not boot",
            description="Use this path when lights or fans start but the system does not reach the operating system.",
            goals=("boot_device_problem", "ram_or_post_issue", "storage_hardware_failure"),
        ),
        SymptomPath(
            id="hardware_display",
            category="hardware",
            label="Screen or display problem",
            description="Use this path for a black, dim, flickering, or distorted display.",
            goals=("internal_display_problem", "graphics_problem"),
        ),
        SymptomPath(
            id="hardware_heat",
            category="hardware",
            label="Overheating or loud fan",
            description="Use this path when the device gets very hot, slows down under heat, or shuts down unexpectedly.",
            goals=("overheating_due_to_airflow", "fan_failure_problem"),
        ),
        SymptomPath(
            id="hardware_peripheral",
            category="hardware",
            label="Peripheral or port problem",
            description="Use this path when a printer, mouse, keyboard, webcam, USB device, or similar accessory is failing.",
            goals=("physical_port_problem", "device_driver_problem", "peripheral_hardware_problem"),
        ),
        SymptomPath(
            id="software_performance",
            category="software",
            label="System is slow or freezes",
            description="",
            goals=("low_storage_problem", "startup_overload", "malware_problem"),
        ),
        SymptomPath(
            id="software_network",
            category="software",
            label="Wi-Fi or internet problem",
            description="Use this path when the computer cannot browse normally or Wi-Fi options are missing.",
            goals=("router_or_isp_problem", "network_adapter_problem", "local_network_configuration_problem"),
        ),
        SymptomPath(
            id="software_application",
            category="software",
            label="Application install or crash problem",
            description="Use this path when one application fails to install, open, or stay stable.",
            goals=("permission_issue", "application_compatibility_problem", "application_corruption_problem"),
        ),
        SymptomPath(
            id="software_security",
            category="software",
            label="Security or malware symptom",
            description="Use this path for pop-ups, redirects, suspicious background activity, or disabled protection.",
            goals=("malware_problem", "antivirus_configuration_problem"),
        ),
        SymptomPath(
            id="software_startup",
            category="software",
            label="Startup, login, or blue-screen problem",
            description="Use this path when the operating system fails during startup, blue-screens, or blocks sign-in.",
            goals=("update_or_driver_conflict", "login_configuration_problem"),
        ),
    )

    return KnowledgeBase(
        questions=questions,
        rules=rules,
        diagnoses=diagnoses,
        symptom_paths=symptom_paths,
    )


KNOWLEDGE_BASE = build_knowledge_base()
